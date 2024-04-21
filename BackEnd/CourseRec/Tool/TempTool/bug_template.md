$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
$session.Cookies.Add((New-Object System.Net.Cookie("JSESSIONID", "7CA008AAD019CC3CBEB28331BB69336D", "/", "tis.sustech.edu.cn")))
$session.Cookies.Add((New-Object System.Net.Cookie("route", "02a1344e82a4379f520dd2ee82590745", "/", "tis.sustech.edu.cn")))
Invoke-WebRequest -UseBasicParsing -Uri "https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList" `
-Method "POST" `
-WebSession $session `
-Headers @{
"Accept"="application/json, text/javascript, */*; q=0.01"
  "Accept-Encoding"="gzip, deflate, br"
  "Accept-Language"="zh-CN,zh;q=0.9"
  "Origin"="https://tis.sustech.edu.cn"
  "Referer"="https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList/3"
  "Sec-Fetch-Dest"="empty"
  "Sec-Fetch-Mode"="cors"
  "Sec-Fetch-Site"="same-origin"
  "X-Requested-With"="XMLHttpRequest"
  "sec-ch-ua"="`"Not_A Brand`";v=`"8`", `"Chromium`";v=`"120`", `"Google Chrome`";v=`"120`""
  "sec-ch-ua-mobile"="?0"
  "sec-ch-ua-platform"="`"Windows`""
  "sec-gpc"="1"
} `
-ContentType "application/x-www-form-urlencoded; charset=UTF-8" `
-Body "p_chapylx=&ordertext_0=&p_xn=2023-2024&p_xq=2&p_xnxq=2023-20242&p_gjz=&p_xiaoqu=&p_kkyx=&p_rwlx=&p_kclb=&p_kcxz=&p_chaxungjz=&p_chaxunxiaoqu=&p_chaxunkkyx=&p_chaxunnj=&p_chaxunglyx=&p_chaxunzy=&p_chaxunxdm=&p_chaxunpylx=3&mxpylx=3&p_id=&p_sfhltsxx=0&file=&pageNum=1&pageSize=1000"



curl 'https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList' \
  -H 'Accept: application/json, text/javascript, */*; q=0.01' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Cookie: JSESSIONID=7CA008AAD019CC3CBEB28331BB69336D; route=02a1344e82a4379f520dd2ee82590745' \
  -H 'Origin: https://tis.sustech.edu.cn' \
  -H 'Referer: https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList/3' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-gpc: 1' \
  --data-raw 'p_chapylx=&ordertext_0=&p_xn=2022-2023&p_xq=3&p_xnxq=2022-20233&p_gjz=&p_xiaoqu=&p_kkyx=&p_rwlx=&p_kclb=&p_kcxz=&p_chaxungjz=&p_chaxunxiaoqu=&p_chaxunkkyx=&p_chaxunnj=&p_chaxunglyx=&p_chaxunzy=&p_chaxunxdm=&p_chaxunpylx=3&mxpylx=3&p_id=&p_sfhltsxx=0&file=&pageNum=1&pageSize=500' \
  --compressed


2023夏季学期
fetch("https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList/3",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "p_chapylx=&ordertext_0=&p_xn=2022-2023&p_xq=3&p_xnxq=2022-20233&p_gjz=&p_xiaoqu=&p_kkyx=&p_rwlx=&p_kclb=&p_kcxz=&p_chaxungjz=&p_chaxunxiaoqu=&p_chaxunkkyx=&p_chaxunnj=&p_chaxunglyx=&p_chaxunzy=&p_chaxunxdm=&p_chaxunpylx=3&mxpylx=3&p_id=&p_sfhltsxx=0&file=&pageNum=1&pageSize=500",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});

2024春季学期
fetch("https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList/3",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "p_chapylx=&ordertext_0=&p_xn=2023-2024&p_xq=2&p_xnxq=2023-20242&p_gjz=&p_xiaoqu=&p_kkyx=&p_rwlx=&p_kclb=&p_kcxz=&p_chaxungjz=&p_chaxunxiaoqu=&p_chaxunkkyx=&p_chaxunnj=&p_chaxunglyx=&p_chaxunzy=&p_chaxunxdm=&p_chaxunpylx=3&mxpylx=3&p_id=&p_sfhltsxx=0&file=&pageNum=1&pageSize=500",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});

2024夏季学期
fetch("https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList/3",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "p_chapylx=&ordertext_0=&p_xn=2023-2024&p_xq=3&p_xnxq=2023-20243&p_gjz=&p_xiaoqu=&p_kkyx=&p_rwlx=&p_kclb=&p_kcxz=&p_chaxungjz=&p_chaxunxiaoqu=&p_chaxunkkyx=&p_chaxunnj=&p_chaxunglyx=&p_chaxunzy=&p_chaxunxdm=&p_chaxunpylx=3&mxpylx=3&p_id=&p_sfhltsxx=0&file=&pageNum=1&pageSize=500",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});

2023秋季学期
fetch("https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList/3",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "p_chapylx=&ordertext_0=&p_xn=2023-2024&p_xq=1&p_xnxq=2023-20241&p_gjz=&p_xiaoqu=&p_kkyx=&p_rwlx=&p_kclb=&p_kcxz=&p_chaxungjz=&p_chaxunxiaoqu=&p_chaxunkkyx=&p_chaxunnj=&p_chaxunglyx=&p_chaxunzy=&p_chaxunxdm=&p_chaxunpylx=3&mxpylx=3&p_id=&p_sfhltsxx=0&file=&pageNum=1&pageSize=500",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});