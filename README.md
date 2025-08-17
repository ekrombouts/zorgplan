# 🏥 Automatische Zorgplan Generatie

Een AI-gestuurde applicatie voor het automatisch genereren van zorgplannen op basis van clientdossiers in verpleeghuizen.

## Functionaliteit

Het systeem analyseert een clientdossier (.txt bestand) en:

1. **Identificeert de drie belangrijkste zorgproblemen** met gestructureerde output (titel en beschrijving)
2. **Genereert zorgplanregels** voor elk probleem met realistisch doel en drie acties, aangepast aan de verpleeghuis context
3. **Vraagt specialistische adviezen op** van:
   - Diëtist (bij gewichtsverlies/verminderde intake)
   - Fysiotherapeut (bij valrisico/mobiliteit problemen)
4. **Presenteert het complete zorgplan** in een overzichtelijke format
5. **Verstuurt het zorgplan per email** naar het zorgteam

## Architectuur

De applicatie gebruikt de OpenAI Agents SDK met verschillende gespecialiseerde agents:

- **ProblemIdentificationAgent**: Identificeert zorgproblemen
- **CarePlanAgent**: Stelt zorgplanregels op
- **DiëtistAgent**: Geeft voedingsadviezen
- **FysiotherapeutAgent**: Geeft mobiliteitsadviezen  
- **FormatAgent**: Formatteert output voor weergave
- **EmailAgent**: Verstuurt het zorgplan per email

## Installatie

1. Installeer de benodigde packages:
```bash
pip install -r requirements.txt
```

2. Kopieer `.env.example` naar `.env` en vul je API keys in:
```bash
cp .env.example .env
```

3. Stel je environment variabelen in:
   - `OPENAI_API_KEY`: Je OpenAI API key
   - `SENDGRID_API_KEY`: Je SendGrid API key voor email functionaliteit

## Gebruik

Start de applicatie:
```bash
python careplan_app.py
```

1. Upload een clientdossier (.txt bestand)
2. Klik op "Genereer Zorgplan"
3. Het systeem toont real-time updates van het proces
4. Het complete zorgplan wordt weergegeven en per email verstuurd

## Voorbeeld Clientdossier

Zie `clientdossier.txt` voor een voorbeeld van het verwachte format.

## Gestructureerde Output

Het systeem gebruikt Pydantic modellen voor gestructureerde output:

- **CareProblems**: Lijst van geïdentificeerde problemen
- **CarePlanRule**: Complete zorgplanregel met probleem, doel en acties
- **SpecialistAdvice**: Specialistisch advies met beoordeling en aanbeveling
- **CompleteCareplan**: Het volledige zorgplan

## Zorgplan Context

Het systeem is specifiek ontworpen voor verpleeghuiszorg, waarbij:
- Doelen gericht zijn op behoud, comfort en kwaliteit van leven (niet altijd verbetering)
- Acties praktisch uitvoerbaar zijn door het zorgteam
- Specialistische input automatisch wordt ingewonnen waar relevant
- De output professioneel en overzichtelijk wordt gepresenteerd
