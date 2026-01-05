#!/bin/bash
mkdir -p images/logos

# Download known logos with User-Agent to avoid blocking
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"

curl -L -H "User-Agent: $UA" -o images/logos/drb_hicom.png "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/DRB-HICOM_Logo.png/320px-DRB-HICOM_Logo.png"
curl -L -H "User-Agent: $UA" -o images/logos/eco_world.png "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Eco_World_Development_Group_Logo.svg/320px-Eco_World_Development_Group_Logo.svg.png"
curl -L -H "User-Agent: $UA" -o images/logos/kpm.png "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Kementerian_Pendidikan_Malaysia.png/200px-Kementerian_Pendidikan_Malaysia.png"
curl -L -H "User-Agent: $UA" -o images/logos/alp_omega.png "https://static.wixstatic.com/media/89a55c_29596328c6e340e495267ed01c36054f~mv2.png/v1/fill/w_136,h_46,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/ALPlogo-01.png"

# Download placeholders for others
curl -L -H "User-Agent: $UA" -o images/logos/glenmarie_cove.png "https://placehold.co/300x150/ffffff/000000/png?text=Glenmarie+Cove"
curl -L -H "User-Agent: $UA" -o images/logos/golden_horse.png "https://placehold.co/300x150/ffffff/000000/png?text=Golden+Horse"
curl -L -H "User-Agent: $UA" -o images/logos/tuck_sun.png "https://placehold.co/300x150/ffffff/000000/png?text=Tuck+Sun"
curl -L -H "User-Agent: $UA" -o images/logos/beon_packaging.png "https://placehold.co/300x150/ffffff/000000/png?text=Beon+Packaging"
curl -L -H "User-Agent: $UA" -o images/logos/dif_logistics.png "https://placehold.co/300x150/ffffff/000000/png?text=DIF+Logistics"
curl -L -H "User-Agent: $UA" -o images/logos/ts_transport.png "https://placehold.co/300x150/ffffff/000000/png?text=TS+Transport"
curl -L -H "User-Agent: $UA" -o images/logos/yong_fong.png "https://placehold.co/300x150/ffffff/000000/png?text=Yong+Fong"
curl -L -H "User-Agent: $UA" -o images/logos/kt_haulage.png "https://placehold.co/300x150/ffffff/000000/png?text=KT+Haulage"
curl -L -H "User-Agent: $UA" -o images/logos/united_heat.png "https://placehold.co/300x150/ffffff/000000/png?text=United+Heat"
