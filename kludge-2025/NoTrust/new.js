import { importPKCS8, SignJWT } from "jose";

const privateKeyPem = `-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDZTqBFKHBSopAl
G9dCnld7sXfoafIrPUz7WSZwbojy9scH/JflloinqZ59RO7DrRzx5h/ytFmxtKBB
Bt7IaXNkeOyYVG9H4GspJICO3AeMkqct2dEjrXfBqNFM/GVwLBw2Iw8oB8Da46cq
ojMaOBKlRCw+iDKnHWLYJPBQTWwy8TwjxvrFJoEMISPOqwLGiOGKdd1edOCbET9W
2BsO0/5UHlKaClc5DSQJhrqpoqPAWjkuPWJf1d643V0XGlbLaaVSYLdEwUq0HalO
5NXBBEnv2mUxgSL7wrli6E9+xNKsn+q87ufMIMpCThy8bHWRrRYbQ8T2qf5YJtn7
300VeCNLAgMBAAECggEADE9qJuDM+osFzWrC8ND76O1U+wNdc6bSWjH8fawIiz/N
mjc5LglidNULPgXbD/yzjt4krmDnH99sOjxp/6jYBgR2ER8SlFwACUgHFfcck/fb
pQfmbOku+pDv4mn97EyjZuTpJX38jKnbo3LZOds2IZfRRdP89cvLxXpta3v0IC9a
XSAmQOEXDfXWASdR1vQkIKRg8H34Yi+c/Q7PhoVKthCxqGv9M+mXpZVvF6IWIjVh
FlisHW9dDbAjzfaKldtbSbm9YVQ7pzhz2IU0M73zZfDnxMs6dc2s+wP+29avfWeS
lztps3YKMdzkImBJ7Spb2VtFGpm51tr1BMOStogf0QKBgQDr/a2vdNh4E5JgYg1s
Y8o52TrOEHsSdywWUoJ/J8MFWTRVtayEb73vdgZV/EfE85yyfgyvfftCfFaEYpIV
uDHbLiTeAtqwmYtrwuayLgRG2ecIqAADXXftimWwwQLDqlwFQJCMaRmDCcnP54oq
C0MsSo3HeHsHRq6alwAxoXI62QKBgQDru2egt/X/qJsROCWCwZmGQCbpn3/4sCYI
xNrmITwp1JM1Cl7z2ZG1MQd0spHCodtSVFT9+t18ipxzTr7bF3gyYY9U0aRkqRQv
7+d43FfZqlja0DXc7Gh5r+zjLtjYmP7DWmM60kwax4zBDnILRQZ66jc/dq3dsb9c
sPhaX63QwwKBgD6AIBjg/FfI7zKBpYZ4Y12wz6c1rDK2x0FeNtuQX1EyT+8HP5qP
saETBBiPyT47Otv3EEsGNZ5lKdDD/masMuAWt4LpBJxS/h7bLpgwIcfV/B9Jxz8c
6R9LUSVf6OiDXP2zHNVjHHOdCwr6CpiaBP9c+3HB0euaZ7HfnhiG5qb5AoGAGCvf
NFuonc5sGBfpwL6ZP2rUkqAIPzfQrpWA3JgL0z442fd2RQrKJgog+ZZV29883fRH
wsM2cs7DvA8XAuAlMwVN7SSR9sBfkYrH8VympWsSMV2oKD8Vd2TSpXjoQ01s0hsy
kZV+uEA97o3Mo9swDup1P8yrh0/yj06WKK4m5IECgYEA3ZnRXIR8CY7nPB6cKL8p
hOWy2TyDBdn4ANS8DJvv6QwRMtJC4INg7gEN1lBdmiLJs+7dRbrdMa9MWt1WUUnj
BnF3ZNbgS/XA7zlmhyn0Khb7p2CzeUnL8cvNdutpvGpYpWL4Oc7TaP6499NMZfMr
ACE/1jov7K5OwGQ9OMJYSkM=
-----END PRIVATE KEY-----`;

const name = "admi";
const timestamp = Math.floor(Date.now() / 100000).toString();
const publicKey = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2U6gRShwUqKQJRvXQp5X
e7F36GnyKz1M+1kmcG6I8vbHB/yX5ZaIp6mefUTuw60c8eYf8rRZsbSgQQbeyGlz
ZHjsmFRvR+BrKSSAjtwHjJKnLdnRI613wajRTPxlcCwcNiMPKAfA2uOnKqIzGjgS
pUQsPogypx1i2CTwUE1sMvE8I8b6xSaBDCEjzqsCxojhinXdXnTgmxE/VtgbDtP+
VB5SmgpXOQ0kCYa6qaKjwFo5Lj1iX9XeuN1dFxpWy2mlUmC3RMFKtB2pTuTVwQRJ
79plMYEi+8K5YuhPfsTSrJ/qvO7nzCDKQk4cvGx1ka0WG0PE9qn+WCbZ+99NFXgj
SwIDAQAB
-----END PUBLIC KEY-----`;

const message = name + timestamp + publicKey;

const key = await importPKCS8(privateKeyPem, "RS256");
const signature = await new SignJWT({
  name: name,
  timestamp: timestamp,
  publicKey: publicKey,
  signature: Buffer.from(message).toString("base64")
})
  .setProtectedHeader({ alg: "RS256" })
  .sign(key);

console.log("JWT Token:\n" + signature);

