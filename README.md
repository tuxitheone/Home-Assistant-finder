# ![Banner](banner.png)

# 🔍 Home Assistant Auto-Finder (Windows + Linux)

Et lille Python-script, der automatisk scanner dit lokale netværk og finder, hvilken IP-adresse din **Home Assistant**-server bruger (port **8123**).

Scriptet kan køres både på **Windows** og **Linux**, så længe Python 3 er installeret.

Perfekt til:
- Headless Home Assistant installationer (ingen skærm på boksen)
- Proxmox / VM-miljøer
- Raspberry Pi og andre små bokse
- Hurtigt at finde ny IP efter reinstall / flytning

---

## 🚀 Funktioner

- Fungerer på både **Windows** og **Linux**
- Finder automatisk din lokale IPv4-adresse
- Antager et /24-netværk (fx `192.168.2.0/24`)
- Scanner hele subnettet efter åben port **8123**
- Kører i loop indtil en Home Assistant-server svarer
- Kan altid stoppes med **CTRL + C**
- Ingen eksterne Python-pakker – kun standardbiblioteket

---

## 📦 Krav

- **Python 3.x**
- Netværksforbindelse til det subnet, hvor Home Assistant kører
- På Windows: Python tilføjet til `PATH` (valgfrit, men rart)
- På Linux: Standard Python 3-installation (Debian/Ubuntu/RPiOS mv.)

---

## 📥 Installation

Pak ZIP-filen ud, så du har disse filer:

```text
find_ha.py
README.md
banner.png
```

---

## ▶️ Brug på Linux

Åbn en terminal i mappen med filerne og kør:

```bash
chmod +x find_ha.py
./find_ha.py
```

Eller:

```bash
python3 find_ha.py
```

Eksempel-output:

```text
🔍 Home Assistant Auto-Finder (Windows + Linux)
   Scanner efter Home Assistant på port 8123
   Kører indtil en server findes – stop med CTRL+C

🌐 Opdaget lokal IP-range (baseret på /24): 192.168.2.0/24

⏳ Ingen Home Assistant fundet endnu... prøver igen om 5 sekunder.
⏳ Ingen Home Assistant fundet endnu... prøver igen om 5 sekunder.
✅ Fundet Home Assistant: http://192.168.2.84:8123

Færdig. Åbn adressen ovenfor i din browser.
```

---

## ▶️ Brug på Windows

1. Sørg for at **Python 3** er installeret  
   (du kan teste i **PowerShell** eller **Kommandoprompt**):

   ```powershell
   python --version
   ```
   eller
   ```powershell
   py --version
   ```

2. Navigér til mappen med `find_ha.py`:

   ```powershell
   cd C:\sti\til\mappen
   ```

3. Kør scriptet:

   ```powershell
   python .\find_ha.py
   ```
   eller

   ```powershell
   py .\find_ha.py
   ```

Stop med **CTRL + C** hvis du vil afbryde.

---

## 🔍 Hvordan virker det?

1. **Finder lokal IPv4-adresse**  
   Scriptet laver en "falsk" UDP-forbindelse til `8.8.8.8:80` for at finde den IP, dit system ville bruge til at gå på nettet.  
   Der sendes ingen rigtig trafik, men OS vælger det rigtige interface.

2. **Antager et /24-subnet**  
   Hvis IP f.eks. er `192.168.2.57`, antager scriptet netværket:

   ```text
   192.168.2.0/24
   ```

   og scanner alle adresser fra `192.168.2.1` til `192.168.2.254`.

3. **Scanner port 8123**  
   For hver IP prøves en TCP-forbindelse til port **8123**.  
   Hvis den svarer, antages det, at det er en Home Assistant-instans.

4. **Looper indtil succes**  
   Hvis der ikke findes nogen, venter scriptet et par sekunder og prøver igen.

---

## 🧪 Typiske scenarier

- Du har lige installeret Home Assistant på en **Raspberry Pi** uden skærm  
- Du har lavet en ny **VM i Proxmox** med Home Assistant  
- Din router har givet en anden IP end du forventede  
- Du sætter Home Assistant op for andre, og vil hurtigt kunne finde IP’en

---

## ❗ Fejlfinding

### Scriptet siger: *"Kunne ikke finde en ikke-127.x IPv4-adresse."*

Mulige årsager:
- Maskinen er ikke forbundet til et netværk
- Der er kun loopback (127.0.0.1) aktivt
- VPN / specielle netværksopsætninger

➜ Tjek din netværksforbindelse og prøv igen.

---

### Scriptet finder ingen Home Assistant

Tjek følgende:
- Kører Home Assistant faktisk?
- Er port **8123** åben i firewall?
- Er den maskine, du kører scriptet fra, på **samme subnet**?
- Bruger du VLANs, hvor der måske ikke er routing mellem netværkene?

---

## 📂 Projektstruktur

```text
homeassistant-autofinder/
├── find_ha.py
├── README.md
└── banner.png
```

---

## 📜 License

MIT License

---

## 💡 Idéer til videreudvikling

- Tilføje scanning af flere porte (fx HTTPS, add-ons osv.)
- Enkel web-UI der viser scanning live
- Docker-version der kan køre i container
- Mulighed for at angive subnet manuelt via argumenter

PR’er og forks er naturligvis velkomne 🙂
