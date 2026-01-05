# Deployment Guide: DigitalOcean + GoDaddy (GitHub Workflow)

This guide will walk you through hosting your static website on a DigitalOcean Droplet using **GitHub** and connecting it to your GoDaddy domain.

## Prerequisites
- A **DigitalOcean** account.
- A **GoDaddy** account with your domain purchased.
- Your code pushed to a **GitHub repository**.
- Terminal/Command Line access.

---

## Step 1: Create a DigitalOcean Droplet

1.  Log in to DigitalOcean.
2.  Click **Create** -> **Droplets**.
3.  **Choose Region**: Select a datacenter closest to your target audience (e.g., Singapore, San Francisco, London).
4.  **Choose Image**: Select **Ubuntu 24.04 (LTS) x64** (or the latest LTS version).
5.  **Choose Size**: Select **Basic**, then **Regular Disk Type**. The cheapest option ($4-6/month) is plenty.
6.  **Authentication Method**:
    *   **SSH Key (Recommended)**: If you have one, select it.
    *   **Password**: Create a strong root password.
7.  **Finalize**: Give your droplet a name (e.g., `aev-website`) and click **Create Droplet**.
8.  **Wait**: In a minute, you will get an **IP Address** (this is your **Public IP**, e.g., `123.45.67.89`). Copy this. (Ignore the "Private IP").

---

## Step 2: Configure GoDaddy DNS

1.  Log in to **GoDaddy**.
2.  Go to your **Domain Portfolio** and select your domain.
3.  Click on **DNS**.
4.  Add/Edit the following **A Records**:
    *   **Type**: `A`
    *   **Name**: `@`
    *   **Value**: `YOUR_DROPLET_IP` (Result from Step 1)
    *   **TTL**: 600 seconds (or default)
5.  Add a **CNAME Record** (for www):
    *   **Type**: `CNAME`
    *   **Name**: `www`
    *   **Value**: `@` (or your domain name)
    *   **TTL**: Default

*Note: DNS changes can take a few minutes to 48 hours to propagate.*

---

## Step 3: Server Setup

Open your local terminal and SSH into your new server:
```bash
ssh root@YOUR_DROPLET_IP
# Make sure to use the PUBLIC IP (e.g., 143.198.xxx.xxx), NOT the Private IP (10.104.xxx.xxx).
# If using password, it will ask for it now.
# If "Permission denied (publickey)": You likely chose SSH Key but don't have the corresponding key on this computer.
# You may need to "Reset Password" in the DigitalOcean dashboard -> Access to switch to password login.
```

Once logged in, run these commands to update the system and install **Nginx** and **Git**:

```bash
apt update
apt install nginx git -y
ufw allow 'Nginx Full'
```

Verify Nginx is running by visiting `http://YOUR_DROPLET_IP` in your browser.

---

## Step 4: Clone Your Repository

We will clone your code into `/var/www/aevlanding`.

1.  Go to the `/var/www` directory:
    ```bash
    cd /var/www
    ```

2.  Clone your repository:
    
    *If your repository is **Public**:*
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git aevlanding
    ```
    
    *If your repository is **Private**:*
    You will need to use a Personal Access Token (PAT) or generate an SSH key on the server (`ssh-keygen`), add the public key to your GitHub repo's "Deploy Keys", and then clone using SSH:
    ```bash
    git clone git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git aevlanding
    ```

3.  Verify the files are there:
    ```bash
    ls /var/www/aevlanding
    ```

---

## Step 5: Configure Nginx

1.  Create a new config file for your site:
    ```bash
    nano /etc/nginx/sites-available/aevlanding
    ```

2.  Paste the following configuration (Modifying `server_name` to match your domain):

    ```nginx
    server {
        listen 80;
        listen [::]:80;
        
        # REPLACE THESE WITH YOUR ACTUAL DOMAIN
        server_name example.com www.example.com;

        root /var/www/aevlanding;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
        
        # Cache images and css
        location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
            expires 7d;
        }
    }
    ```

3.  Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

4.  Enable the site and remove the default config:
    ```bash
    ln -s /etc/nginx/sites-available/aevlanding /etc/nginx/sites-enabled/
    rm /etc/nginx/sites-enabled/default  # IMPORTANT: Remove default to avoid conflicts
    ```

5.  Test and restart Nginx:
    ```bash
    nginx -t
    systemctl restart nginx
    ```

**Your site should now be live at `http://yourdomain.com`!**

---

## Step 6: Secure with SSL (HTTPS)

1.  Install Certbot:
    ```bash
    apt install certbot python3-certbot-nginx -y
    ```

2.  Run Certbot:
    ```bash
    certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

---

## Updating Your Site in the Future

When you push changes to GitHub from your computer, update the server like this:

1.  SSH into your server:
    ```bash
    ssh root@YOUR_DROPLET_IP
    ```

2.  Go to your project folder and pull the changes:
    ```bash
    cd /var/www/aevlanding
    git pull
    ```

That's it! Your site is updated immediately.
