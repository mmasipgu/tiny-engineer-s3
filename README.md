# Tiny Engineer S3 — instalador web

Este repositorio publica automáticamente una variante de `jamro/tiny-engineer`
para **ESP32-S3-N16R8**, usando PCA9685 y MAX98357A externos.

## Pinout

| Función | GPIO |
|---|---:|
| I2C SDA | 8 |
| I2C SCL | 9 |
| PCA9685 OE | 16 |
| MAX98357A BCLK | 17 |
| MAX98357A LRC/WS | 18 |
| MAX98357A DIN | 21 |
| USB D- | 19 |
| USB D+ | 20 |

## Publicación inicial

1. Crea en GitHub un repositorio **vacío**, por ejemplo `tiny-engineer-s3`.
2. Abre PowerShell dentro de esta carpeta:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\publish.ps1 -RepoUrl "https://github.com/TU_USUARIO/tiny-engineer-s3.git"
```

3. En GitHub abre `Settings -> Pages` y selecciona `GitHub Actions` como Source.
4. Espera a que termine `Build and publish Tiny Engineer S3 Web Installer`.

La web quedará normalmente en:

`https://TU_USUARIO.github.io/tiny-engineer-s3/`

A partir de ahí no necesitas PlatformIO ni esptool para instalar: abre esa URL
con Chrome/Edge, conecta el ESP32-S3 por USB y pulsa **Instalar firmware**.

## Primer arranque

Después de flashear, Tiny Engineer abre `TinyEngineer-XXXX`. Conéctate y abre:

`http://192.168.4.1/config`

## Alimentación

- USB del PC -> ESP32-S3.
- Fuente 5 V externa -> PCA9685 V+ / servos y MAX98357A.
- GND común entre todo.
- No unas el +5 V externo al VBUS del PC mientras ambas fuentes estén activas.
