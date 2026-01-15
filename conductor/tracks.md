# Project Tracks: Comparador Inteligente (Optimizado para Despliegue Gratuito)

## Track 1: Infraestructura Cloud y Core de Identidad
- [ ] **Despliegue Híbrido:** Configurar el Frontend en Vercel (Edge Network) y Microservicios en Render (Free Tier).
- [ ] **Keep-Alive System:** Implementar un "Ping-Service" interno (Cron-Job simulado) que realice una petición HTTP cada 14 min para evitar el 'sleep' de Render.
- [ ] **Auth & Data con Supabase:** Sustituir el microservicio manual de Auth por Supabase Auth (JWT/Bcrypt nativo) para ahorrar RAM en el servidor.
- [ ] **Esquema Relacional:** Inicializar tablas en Supabase (PostgreSQL) para usuarios,  y .
- [ ] **Caché de Historial:** Configurar SQLite (en volumen persistente) o la base de datos local de Cloud Shell para el historial del Agente SRBC.

## Track 2: Adquisición de Datos "Low-Resource" y Orquestador
- [ ] **Orchestrator Search:** Crear endpoint POST /api/v1/search_product optimizado para no exceder los 512MB de RAM de Render.
- [ ] **API First:** Priorizar el uso de APIs gratuitas/freemium (como SerpApi o Datafiniti) para evitar el sobrecoste de proxies residenciales iniciales.
- [ ] **Scraper Ligero (Cheerio/Axios):** Reemplazar Selenium por Cheerio/Puppeteer-core para eludir bloqueos mediante rotación de User-Agents y Headers, consumiendo mínima memoria.
- [ ] **Data Normalizer:** Crear funciones de estandarización para unificar formatos de moneda y metadatos de diferentes tiendas.
- [ ] **Caché Inteligente:** Implementar persistencia en PostgreSQL para consultas idénticas (TTL de 24h) para ahorrar llamadas a APIs externas.

## Track 3: Sistema Multiagente (SMA) y Lógica de Consenso
- [ ] **Agent Orchestrator:** Implementar la lógica de agentes (Finanzas y Calidad) utilizando 'Function Calling' de Gemini 3 Flash para reducir tokens.
- [ ] **Algoritmo de Consenso:** Desarrollar el cálculo de 'avgScore' y 'bestLink' basado en peso de reseñas vs. precio.
- [ ] **Módulo TrustScore:** Heurística de fiabilidad para detectar "ofertas demasiado buenas para ser verdad".
- [ ] **Agente SRBC:** Implementar motor de recomendación usando 'Vector Search' (usando la extensión pgvector gratuita de Supabase) sobre el historial.
- [ ] **ReviewAnalysis:** Procesamiento asíncrono de reseñas para no bloquear el hilo principal de la respuesta al usuario.

## Track 4: Frontend Profesional (UX/CRO) y Real-Time
- [ ] **Next.js Dashboard:** Interfaz profesional con Tailwind CSS optimizada para Conversión (CRO).
- [ ] **Búsqueda Semántica:** Implementar barra de búsqueda con debouncing y sugerencias dinámicas.
- [ ] **Panel de Comparación:** UI técnica tipo tabla comparativa con resaltado de la "Opción Ganadora".
- [ ] **Visualización de Progreso (SSE):** Usar Server-Sent Events (SSE) para mostrar al usuario cómo los agentes están "analizando" en tiempo real sin recargar.
- [ ] **Filtros Inteligentes:** Árboles de decisión para guiar al usuario según su presupuesto y prioridad (Calidad vs. Precio).

## Track 5: Monetización y Soporte con IA
- [ ] **Freemium Logic:** Implementar Rate Limiting basado en el ID de usuario de Supabase (5 búsquedas/semana).
- [ ] **Affiliation Injector:** Módulo para inyectar IDs de afiliado (Amazon, eBay, etc.) automáticamente en el botón de compra.
- [ ] **Stripe Integration:** Configurar 'Checkout Session' para usuarios que deseen pasar al plan Pro (búsquedas ilimitadas).
- [ ] **Soporte IA Multimodal:** Chatbot de soporte integrado con la base de conocimientos del producto y capacidad de transcripción (Whisper API).
