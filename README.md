# Diésel Cerca

App web para el móvil que te enseña en un mapa las gasolineras cercanas con el precio del diésel (Gasóleo A y Premium), la más barata, la media de la zona, cuánto ahorras por depósito y si ha subido o bajado desde ayer.

Los precios salen de la API oficial del Ministerio (MITECO). GitHub Actions los descarga cada hora y los guarda en `data/diesel.json`; la app los lee desde ahí. Todo en la nube, sin nada en tu PC.

## Puesta en marcha (unos 5 minutos)

1. Crea un repositorio nuevo en GitHub, por ejemplo `diesel-cerca`. Puede ser público.
2. Sube todos los archivos de esta carpeta respetando las carpetas (`.github/workflows/`).
3. **Settings → Actions → General → Workflow permissions**: marca *Read and write permissions* y guarda.
4. **Actions → Actualizar precios diésel → Run workflow**. En un minuto aparecerá `data/diesel.json`.
5. **Settings → Pages**: *Source* = *Deploy from a branch*, rama `main`, carpeta `/ (root)`. Guarda.
6. Abre `https://TU-USUARIO.github.io/diesel-cerca/` en el móvil y dale permiso de ubicación.
7. Añádela a la pantalla de inicio (Chrome: menú ⋮ → *Añadir a pantalla de inicio*; Safari: Compartir → *Añadir a inicio*). Se abre a pantalla completa como una app.

## Qué hace

- Te localiza y muestra las gasolineras en 3, 5, 10 o 20 km, con el precio en cada una (verde = de las más baratas, rojo = de las más caras de la zona).
- Arriba cambias entre **Diésel** y **Diésel+**.
- Lista ordenable por precio o por distancia, filtro **Abiertas ahora** y cálculo del ahorro según tu depósito (40–70 L).
- Flecha ▼/▲ con la variación respecto al precio de ayer (aparece a partir del segundo día).
- Toca una gasolinera para ver sus precios y horario, y **Cómo llegar** abre Google Maps.
- Si mueves el mapa, **Buscar en esta zona** recalcula allí.
- Recuerda radio, orden, carburante y depósito en el móvil.

## Si algo falla

- **La app se queda cargando**: comprueba que el paso 4 terminó en verde y que existe `data/diesel.json`.
- **El workflow falla al descargar**: la API del Ministerio a veces tarda o corta; el script reintenta 4 veces. Si falla, vuelve a lanzarlo a mano.
- GitHub puede retrasar unos minutos las ejecuciones programadas; es normal.
