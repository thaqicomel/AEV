from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import sqlite3
import os
import shutil
from database import get_db_connection

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Helper to get content for a page
def get_page_content(page_name):
    conn = get_db_connection()
    rows = conn.execute("SELECT key, value, type FROM content WHERE page = ?", (page_name,)).fetchall()
    conn.close()
    content = {row['key']: row['value'] for row in rows}
    return content


# Helper to get gallery images
def get_gallery_images(page_name, section):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM gallery WHERE page = ? AND section = ?", (page_name, section)).fetchall()
    conn.close()
    return rows

# Helper to get subsection images
def get_subsection_images(page_name, subsection):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM gallery WHERE page = ? AND subsection = ?", (page_name, subsection)).fetchall()
    conn.close()
    return rows

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    content = get_page_content('index')
    print("DEBUG CONTENT:", content)
    
    # Fetch team members
    conn = get_db_connection()
    team_members = [dict(row) for row in conn.execute("SELECT * FROM team_members").fetchall()]
    
    # Fetch team slideshow images
    team_slideshow = [dict(row) for row in conn.execute("SELECT * FROM gallery WHERE page='index' AND section='team_slideshow'").fetchall()]
    conn.close()

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "content": content,
        "team_members": team_members,
        "team_slideshow": team_slideshow
    })

@app.get("/{page_name}.html", response_class=HTMLResponse)
async def read_page(request: Request, page_name: str):
    content = get_page_content(page_name)
    # Check if template exists
    if not os.path.exists(f"templates/{page_name}.html"):
         raise HTTPException(status_code=404, detail="Page not found")
    
    # Fetch gallery images for this page (assuming section is 'gallery' for now)
    gallery_images = get_gallery_images(page_name, 'gallery')
    
    # Fetch all subsection images for this page
    conn = get_db_connection()
    subsection_images = [dict(row) for row in conn.execute("SELECT * FROM gallery WHERE page = ? AND subsection IS NOT NULL", (page_name,)).fetchall()]
    conn.close()
    
    # Group subsection images by subsection for easy access in template
    subsection_images_grouped = {}
    for img in subsection_images:
        subsection = img['subsection']
        if subsection not in subsection_images_grouped:
            subsection_images_grouped[subsection] = []
        subsection_images_grouped[subsection].append(img)
    
    return templates.TemplateResponse(f"{page_name}.html", {
        "request": request, 
        "content": content,
        "gallery_images": gallery_images,
        "subsection_images": subsection_images_grouped
    })

# --- Admin Routes ---

@app.get("/admin", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})

@app.post("/admin/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    
    if user and user['password'] == password: 
        response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="admin_session", value=username)
        return response
    else:
        return templates.TemplateResponse("admin/login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/admin/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("admin_session")
    return response

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = request.cookies.get("admin_session")
    if not user:
        return RedirectResponse(url="/admin")
    
    conn = get_db_connection()
    content_rows = [dict(row) for row in conn.execute("SELECT * FROM content ORDER BY page, section").fetchall()]
    gallery_rows = [dict(row) for row in conn.execute("SELECT * FROM gallery ORDER BY page, section").fetchall()]
    team_rows = [dict(row) for row in conn.execute("SELECT * FROM team_members").fetchall()]
    conn.close()
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request, 
        "user": user, 
        "content_items": content_rows,
        "gallery_items": gallery_rows,
        "team_items": team_rows
    })

@app.post("/admin/update_content")
async def update_content(request: Request, key: str = Form(...), value: str = Form(...)):
    user = request.cookies.get("admin_session")
    if not user:
         raise HTTPException(status_code=401)
         
    conn = get_db_connection()
    # Ensure we only update existing keys allowed by admin interface
    conn.execute("UPDATE content SET value = ? WHERE key = ?", (value, key))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/add_gallery_image")
async def add_gallery_image(request: Request, page: str = Form(...), section: str = Form(...), subsection: str = Form(None), title: str = Form(None), description: str = Form(None), image: UploadFile = File(...)):
    print(f"DEBUG: add_gallery_image - page={page}, section={section}, subsection={subsection}, title={title}")
    user = request.cookies.get("admin_session")
    if not user:
         raise HTTPException(status_code=401)
    
    # Normalize subsection
    if not subsection or subsection.strip() == "":
        subsection = None

    conn = get_db_connection()
    # Check current count
    if subsection:
        count = conn.execute("SELECT COUNT(*) FROM gallery WHERE page = ? AND subsection = ?", (page, subsection)).fetchone()[0]
    else:
        count = conn.execute("SELECT COUNT(*) FROM gallery WHERE page = ? AND section = ? AND subsection IS NULL", (page, section)).fetchone()[0]

    # Determine limit based on section
    limit = 7 if (page == 'index' and section == 'team_slideshow') else 4
    
    if count >= limit:
        conn.close()
        return RedirectResponse(url=f"/admin/dashboard?error=Limit%20Reached%20(Max%20{limit})", status_code=status.HTTP_303_SEE_OTHER)

    file_location = f"static/images/{image.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
        
    conn.execute("INSERT INTO gallery (page, section, subsection, image_path, title, description) VALUES (?, ?, ?, ?, ?, ?)", 
                 (page, section, subsection, f"/static/images/{image.filename}", title, description))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/delete_gallery_image")
async def delete_gallery_image(request: Request, id: int = Form(...)):
    user = request.cookies.get("admin_session")
    if not user:
         raise HTTPException(status_code=401)
         
    conn = get_db_connection()
    result = conn.execute("DELETE FROM gallery WHERE id = ?", (id,))
    print(f"DEBUG: delete_gallery_image - id={id}, rows_affected={result.rowcount}")
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/update_gallery_description")
async def update_gallery_description(request: Request, id: int = Form(...), title: str = Form(None), description: str = Form(None)):
    user = request.cookies.get("admin_session")
    if not user:
         raise HTTPException(status_code=401)
         
    conn = get_db_connection()
    conn.execute("UPDATE gallery SET title = ?, description = ? WHERE id = ?", (title, description, id))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/add_team_member")
async def add_team_member(request: Request, name: str = Form(...), role: str = Form(...), linkedin_url: str = Form(None), image: UploadFile = File(...)):
    print(f"DEBUG: add_team_member - name={name}, role={role}")
    user = request.cookies.get("admin_session")
    if not user:
         raise HTTPException(status_code=401)
    
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM team_members").fetchone()[0]
    if count >= 8:
        conn.close()
        return RedirectResponse(url="/admin/dashboard?error=Limit%20Reached%20(Max%208%20Members)", status_code=status.HTTP_303_SEE_OTHER)

    file_location = f"static/images/{image.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
        
    conn.execute("INSERT INTO team_members (name, role, linkedin_url, image_path) VALUES (?, ?, ?, ?)", 
                 (name, role, linkedin_url, f"/static/images/{image.filename}"))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/update_team_member")
async def update_team_member(request: Request, id: int = Form(...), name: str = Form(...), role: str = Form(...), linkedin_url: str = Form(None), image: UploadFile = File(None)):
    print(f"DEBUG: update_team_member - id={id}, name={name}, role={role}")
    user = request.cookies.get("admin_session")
    if not user:
         raise HTTPException(status_code=401)
         
    conn = get_db_connection()
    
    if image and image.filename:
        file_location = f"static/images/{image.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(image.file, file_object)
        image_path = f"/static/images/{image.filename}"
        conn.execute("UPDATE team_members SET name = ?, role = ?, linkedin_url = ?, image_path = ? WHERE id = ?", (name, role, linkedin_url, image_path, id))
    else:
        conn.execute("UPDATE team_members SET name = ?, role = ?, linkedin_url = ? WHERE id = ?", (name, role, linkedin_url, id))
        
    conn.commit()
    conn.close()
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/delete_team_member")
async def delete_team_member(request: Request, id: int = Form(...)):
    user = request.cookies.get("admin_session")
    if not user:
         raise HTTPException(status_code=401)
    
    conn = get_db_connection()
    result = conn.execute("DELETE FROM team_members WHERE id = ?", (id,))
    print(f"DEBUG: delete_team_member - id={id}, rows_affected={result.rowcount}")
    conn.commit()
    conn.close()
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
