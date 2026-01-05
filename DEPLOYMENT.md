# Deployment Guide: DigitalOcean + GoDaddy

This guide will walk you through hosting your static website on a DigitalOcean Droplet and connecting it to your GoDaddy domain.

## Prerequisites
- A **DigitalOcean** account.
- A **GoDaddy** account with your domain purchased.
- Terminal/Command Line access on your local computer.

---

## Step 1: Create a DigitalOcean Droplet

1.  Log in to DigitalOcean.
2.  Click **Create** -> **Droplets**.
3.  **Choose Region**: Select a datacenter closest to your target audience (e.g., Singapore, San Francisco, London).
4.  **Choose Image**: Select **Ubuntu 24.04 (LTS) x64** (or the latest LTS version).
5.  **Choose Size**: Select **Basic**, then **Regular Disk Type**. The cheapest option ($4-6/month) is plenty for a static site.
6.  **Authentication Method**:
    *   **SSH Key (Recommended)**: If you have one, select it.
    *   **Password**: Create a strong root password.
7.  **Finalize**: Give your droplet a name (e.g., `aev-website`) and click **Create Droplet**.
8.  **Wait**: In a minute, you will get an **IP Address** (e.g., `123.45.67.89`). Copy this.

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

*Note: DNS changes can take a few minutes to 48 hours to propagate, but usually it's quick.*

---

## Step 3: Server Setup (Nginx)

Open your local terminal and SSH into your new server:
```bash
ssh root@YOUR_DROPLET_IP
# If using password, it will ask for it now.
```

Once logged in, run these commands to update the system and install Nginx:

```bash
apt update
apt install nginx -y
ufw allow 'Nginx Full'
```

Verify Nginx is running:
1.  Open your browser and visit `http://YOUR_DROPLET_IP`.
2.  You should see the "Welcome to nginx!" page.

---

## Step 4: Upload Your Website

Back on your **local computer** (open a new terminal window), navigate to your project folder:

```bash
cd /Users/thaqiyuddin/Personal/thaqi/Project/aevlanding
```

Use `scp` (Secure Copy) to upload your files to the server. We'll put them in `/var/www/aevlanding`.

```bash
# Create the directory on the server first
ssh root@YOUR_DROPLET_IP "mkdir -p /var/www/aevlanding"

# Upload all files
scp -r * root@YOUR_DROPLET_IP:/var/www/aevlanding
```

*Note: Enter your server password if prompted.*

---

## Step 5: Configure Nginx

1.  SSH back into your server: `ssh root@YOUR_DROPLET_IP`
2.  Copy the provided config or create a new one. We will create a new config file for your site.

    ```bash
    nano /etc/nginx/sites-available/aevlanding
    ```

3.  Paste the following configuration (Modifying `server_name` to match your domain):

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

4.  Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

5.  Enable the site:
    ```bash
    ln -s /etc/nginx/sites-available/aevlanding /etc/nginx/sites-enabled/
    ```

6.  Test the configuration:
    ```bash
    nginx -t
    ```
    *If successful, it will say "syntax is ok".*

7.  Restart Nginx:
    ```bash
    systemctl restart nginx
    ```

**At this point, your site should be live at `http://yourdomain.com`!**

---

## Step 6: Secure with SSL (HTTPS) - Optional but Recommended

We will use Certbot (Let's Encrypt) for free SSL.

1.  Install Certbot:
    ```bash
    apt install certbot python3-certbot-nginx -y
    ```

2.  Run Certbot:
    ```bash
    certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```
    *Follow the prompts (enter email, agree to terms). Select option "2" to redirect HTTP to HTTPS if asked.*

Your site is now secure! `https://yourdomain.com`

---

## Updating Your Site in the Future

Whenever you make changes locally:

1.  Run the upload command again:
    ```bash
    scp -r * root@YOUR_DROPLET_IP:/var/www/aevlanding
    ```
2.  That's it! (No need to restart Nginx for simple HTML/CSS changes).
