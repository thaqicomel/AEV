import os
import urllib.request
import urllib.error

LOGO_DIR = "images/logos"
if not os.path.exists(LOGO_DIR):
    os.makedirs(LOGO_DIR)

logos = {
    "drb_hicom.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/DRB-HICOM_Logo.png/320px-DRB-HICOM_Logo.png",
    "eco_world.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Eco_World_Development_Group_Logo.svg/320px-Eco_World_Development_Group_Logo.svg.png",
    "kpm.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Kementerian_Pendidikan_Malaysia.png/200px-Kementerian_Pendidikan_Malaysia.png",
    "alp_omega.png": "https://static.wixstatic.com/media/89a55c_29596328c6e340e495267ed01c36054f~mv2.png/v1/fill/w_136,h_46,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/ALPlogo-01.png",
    # Best guesses / Fallbacks for others
    "glenmarie_cove.png": "https://placehold.co/400x120?text=Glenmarie+Cove", 
    "golden_horse.png": "https://placehold.co/400x120?text=Golden+Horse+Rubber",
    "tuck_sun.png": "https://placehold.co/400x120?text=Tuck+Sun+Logistic",
    "beon_packaging.png": "https://placehold.co/400x120?text=Beon+Packaging",
    "dif_logistics.png": "https://placehold.co/400x120?text=DIF+Logistics",
    "ts_transport.png": "https://placehold.co/400x120?text=TS+Transport", 
    "yong_fong.png": "https://placehold.co/400x120?text=Yong+Fong+Rubbers",
    "kt_haulage.png": "https://placehold.co/400x120?text=KT+Haulage",
    "united_heat.png": "https://placehold.co/400x120?text=United+Heat+Transfer"
}

# Try specific URLs for some if they exist
guesses = {
    "tuck_sun.png": ["https://www.tucksun.com/images/logo.png", "https://www.tucksun.com/img/logo.png"],
    "kt_haulage.png": ["https://www.ktlog.com.my/images/logo.png", "https://www.ktlog.com.my/img/logo.png"],
    "united_heat.png": ["https://www.uniheat.com.my/images/logo.png", "https://www.uniheat.com.my/img/logo.png"],
    "glenmarie_cove.png": ["http://glenmarieproperties.com/images/logo.png"]
}

def download_file(url, filename):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            with open(filename, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Downloaded {filename} from {url}")
        return True
    except Exception as e:
        print(f"Failed to download {filename} from {url}: {e}")
        return False

for name, default_url in logos.items():
    filepath = os.path.join(LOGO_DIR, name)
    success = False
    
    # Try guesses first if available
    if name in guesses:
        for url in guesses[name]:
            if download_file(url, filepath):
                success = True
                break
    
    # If guesses fail or don't exist, use default (which might be placeholder)
    if not success:
        download_file(default_url, filepath)
