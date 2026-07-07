from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
from threading import Timer


PORT = 8000


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>LexCheck IA | Auditor de Contratos</title>
  <style>
    :root {
      --ink: #18202a;
      --muted: #697386;
      --line: #d8d5df;
      --panel: #fffefd;
      --page: #f7f3f8;
      --brand: #4b244a;
      --brand-2: #0f766e;
      --accent: #b58b2a;
      --danger: #b42335;
      --warning: #9a6618;
      --ok: #207a56;
      --soft-danger: #fff0f3;
      --soft-warning: #fff8e8;
      --soft-ok: #eaf8f1;
      --shadow: 0 20px 48px rgba(45, 24, 54, .13);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 18% 8%, rgba(181, 139, 42, .18), transparent 28%),
        linear-gradient(135deg, rgba(75, 36, 74, .14), transparent 34%),
        linear-gradient(315deg, rgba(15, 118, 110, .12), transparent 38%),
        var(--page);
    }

    header {
      min-height: 84px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      padding: 22px clamp(18px, 4vw, 54px);
      border-bottom: 1px solid rgba(217, 224, 234, .85);
      background: rgba(255, 255, 255, .76);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 10;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 800;
      font-size: 21px;
    }

    .brand-mark {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      color: white;
      background: linear-gradient(135deg, var(--brand), var(--accent));
      box-shadow: 0 10px 25px rgba(75, 36, 74, .25);
    }

    .status-pill {
      display: flex;
      align-items: center;
      gap: 9px;
      padding: 10px 13px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: white;
      color: var(--muted);
      font-size: 14px;
      white-space: nowrap;
    }

    .dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: var(--brand-2);
      box-shadow: 0 0 0 5px rgba(15, 118, 110, .14);
    }

    main {
      width: min(1180px, calc(100% - 32px));
      margin: 34px auto 56px;
    }

    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1.04fr) minmax(320px, .96fr);
      gap: 22px;
      align-items: stretch;
    }

    .intro {
      padding: clamp(26px, 4vw, 44px);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
      border: 1px solid rgba(217, 224, 234, .8);
    }

    h1 {
      margin: 0;
      max-width: 680px;
      font-size: clamp(34px, 5vw, 64px);
      line-height: .96;
      letter-spacing: 0;
    }

    .lead {
      max-width: 670px;
      margin: 20px 0 0;
      color: var(--muted);
      font-size: clamp(16px, 2vw, 19px);
      line-height: 1.58;
    }

    .benefits {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 28px;
    }

    .benefit {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fffdfa;
    }

    .benefit strong {
      display: block;
      margin-bottom: 5px;
      font-size: 14px;
    }

    .benefit span {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }

    .upload-panel, .results-panel, .clause-panel, .lawyer-panel {
      border: 1px solid rgba(217, 224, 234, .9);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
    }

    .upload-panel {
      padding: 22px;
      display: flex;
      flex-direction: column;
      min-height: 100%;
    }

    .panel-title {
      margin: 0 0 7px;
      font-size: 18px;
    }

    .panel-copy {
      margin: 0 0 18px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }

    .dropzone {
      display: grid;
      place-items: center;
      text-align: center;
      min-height: 205px;
      padding: 24px;
      border: 2px dashed #aebcca;
      border-radius: 8px;
      background: #fbf8fc;
      cursor: pointer;
      transition: .18s ease;
    }

    .dropzone:hover, .dropzone.dragging {
      border-color: var(--brand-2);
      background: #f2fbf8;
      transform: translateY(-1px);
    }

    .upload-icon {
      width: 54px;
      height: 54px;
      margin: 0 auto 14px;
      display: grid;
      place-items: center;
      color: var(--brand);
      border-radius: 8px;
      background: #f0e9f1;
    }

    .dropzone b {
      display: block;
      font-size: 17px;
      margin-bottom: 6px;
    }

    .dropzone small {
      color: var(--muted);
      line-height: 1.4;
    }

    input[type="file"] { display: none; }

    .input-section {
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid var(--line);
    }

    .input-section:first-of-type {
      margin-top: 0;
      padding-top: 0;
      border-top: 0;
    }

    .field-title {
      margin: 0 0 4px;
      font-size: 14px;
      font-weight: 850;
      color: var(--ink);
    }

    .field-help {
      margin: 0 0 10px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.42;
    }

    textarea, input, select {
      font: inherit;
      color: var(--ink);
      outline: none;
    }

    textarea {
      width: 100%;
      min-height: 126px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px;
    }

    .purpose-textarea {
      min-height: 94px;
    }

    textarea:focus, input:focus, select:focus {
      border-color: var(--brand-2);
      box-shadow: 0 0 0 4px rgba(15, 118, 110, .13);
    }

    .actions {
      display: flex;
      gap: 12px;
      margin-top: 15px;
      flex-wrap: wrap;
    }

    button, .contact-link {
      min-height: 44px;
      border: 0;
      border-radius: 8px;
      padding: 0 17px;
      font: inherit;
      font-weight: 750;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 9px;
      transition: .16s ease;
      text-decoration: none;
    }

    .primary {
      color: white;
      background: var(--brand);
      box-shadow: 0 12px 24px rgba(75, 36, 74, .24);
    }

    .primary:hover { background: #371936; }

    .secondary {
      color: var(--brand);
      background: #f4eef6;
      border: 1px solid #e3d6e7;
    }

    .secondary:hover { background: #eadfec; }

    .dashboard {
      display: grid;
      grid-template-columns: 340px minmax(0, 1fr);
      gap: 22px;
      margin-top: 22px;
    }

    .results-panel {
      padding: 20px;
    }

    .score {
      display: grid;
      grid-template-columns: 118px 1fr;
      gap: 18px;
      align-items: center;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--line);
    }

    .ring {
      width: 118px;
      height: 118px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: conic-gradient(var(--danger) 0 38%, var(--warning) 38% 68%, var(--ok) 68% 100%);
      position: relative;
    }

    .ring::after {
      content: "";
      width: 86px;
      height: 86px;
      position: absolute;
      border-radius: 50%;
      background: white;
    }

    .ring span {
      position: relative;
      z-index: 1;
      font-weight: 850;
      font-size: 28px;
    }

    .risk-label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 4px;
    }

    .risk-title {
      margin: 0;
      font-size: 25px;
    }

    .risk-copy {
      margin: 8px 0 0;
      color: var(--muted);
      line-height: 1.45;
      font-size: 14px;
    }

    .metrics {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-top: 16px;
    }

    .metric {
      padding: 13px;
      border-radius: 8px;
      background: #f8fafc;
      border: 1px solid var(--line);
    }

    .metric b {
      display: block;
      font-size: 24px;
      margin-bottom: 2px;
    }

    .metric span {
      color: var(--muted);
      font-size: 12px;
    }

    .clause-panel {
      overflow: hidden;
    }

    .toolbar {
      min-height: 64px;
      padding: 15px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      border-bottom: 1px solid var(--line);
      background: #fbfcfe;
    }

    .tabs {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .tab {
      min-height: 36px;
      padding: 0 12px;
      color: var(--muted);
      background: white;
      border: 1px solid var(--line);
      box-shadow: none;
    }

    .tab.active {
      color: white;
      border-color: var(--brand);
      background: var(--brand);
    }

    .list {
      display: grid;
      gap: 12px;
      padding: 18px;
    }

    .finding {
      border: 1px solid var(--line);
      border-left: 5px solid var(--warning);
      border-radius: 8px;
      padding: 15px;
      background: white;
    }

    .finding.high {
      border-left-color: var(--danger);
      background: var(--soft-danger);
    }

    .finding.medium {
      border-left-color: var(--warning);
      background: var(--soft-warning);
    }

    .finding.low {
      border-left-color: var(--ok);
      background: var(--soft-ok);
    }

    .finding-head {
      display: flex;
      justify-content: space-between;
      gap: 14px;
      margin-bottom: 8px;
    }

    .finding h3 {
      margin: 0;
      font-size: 16px;
    }

    .tag {
      flex: 0 0 auto;
      align-self: start;
      padding: 5px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      background: white;
      border: 1px solid rgba(0, 0, 0, .08);
    }

    .finding p {
      margin: 0;
      color: #475467;
      line-height: 1.48;
      font-size: 14px;
    }

    .suggestion {
      margin-top: 11px;
      padding: 11px;
      border-radius: 8px;
      background: rgba(255, 255, 255, .68);
      border: 1px solid rgba(0, 0, 0, .06);
      color: #344054;
      font-size: 13px;
      line-height: 1.45;
    }

    .lawyer-panel {
      margin-top: 22px;
      padding: 22px;
      display: block;
    }

    .lawyer-list {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 16px;
    }

    .lawyer-card {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 15px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fffdfa;
    }

    .lawyer-card h3 {
      margin: 0 0 5px;
      font-size: 17px;
    }

    .lawyer-card p {
      margin: 0;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }

    .lawyer-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 9px;
      margin-top: auto;
    }

    .lawyer-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .lawyer-meta span {
      padding: 6px 9px;
      border-radius: 999px;
      background: #f4eef6;
      color: var(--brand);
      font-size: 12px;
      font-weight: 750;
    }

    .feedback-float {
      width: min(420px, calc(100% - 28px));
      position: fixed;
      right: 18px;
      bottom: 18px;
      z-index: 30;
      display: none;
      padding: 18px;
      border: 1px solid rgba(75, 36, 74, .18);
      border-radius: 8px;
      background: rgba(255, 254, 253, .96);
      box-shadow: 0 24px 60px rgba(45, 24, 54, .24);
      backdrop-filter: blur(14px);
    }

    .feedback-float.visible {
      display: block;
    }

    .feedback-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      margin-bottom: 10px;
    }

    .feedback-head h2 {
      margin: 0;
      font-size: 17px;
    }

    .feedback-head p {
      margin: 5px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.42;
    }

    .icon-button {
      width: 34px;
      min-height: 34px;
      padding: 0;
      border: 1px solid var(--line);
      color: var(--muted);
      background: white;
      box-shadow: none;
    }

    .feedback-field {
      display: grid;
      gap: 7px;
      margin-top: 11px;
    }

    .feedback-field label {
      font-size: 13px;
      font-weight: 800;
    }

    .feedback-field select,
    .feedback-field textarea {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
      padding: 10px 11px;
    }

    .feedback-field textarea {
      min-height: 82px;
    }

    .feedback-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 13px;
    }

    .empty {
      padding: 46px 18px;
      text-align: center;
      color: var(--muted);
    }

    .footer-note {
      margin-top: 14px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }

    @media (max-width: 920px) {
      .hero, .dashboard, .lawyer-list { grid-template-columns: 1fr; }
      .benefits { grid-template-columns: 1fr; }
    }

    @media (max-width: 560px) {
      header { align-items: flex-start; flex-direction: column; }
      .score { grid-template-columns: 1fr; text-align: center; }
      .ring { margin: 0 auto; }
      .metrics { grid-template-columns: 1fr; }
      .toolbar { align-items: flex-start; flex-direction: column; }
      button, .contact-link { width: 100%; }
      .tab { width: auto; }
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-mark" aria-hidden="true">
        <svg width="25" height="25" viewBox="0 0 24 24" fill="none">
          <path d="M7 4h10a2 2 0 0 1 2 2v14H7a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z" stroke="currentColor" stroke-width="2"/>
          <path d="M9 8h6M9 12h6M9 16h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      LexCheck IA
    </div>
    <div class="status-pill"><span class="dot"></span> Lushiana Escobedo Castro y Alel Nadim Orbezo</div>
  </header>

  <main>
    <section class="hero">
      <div class="intro">
        <h1>Auditor inmediato de contratos antes de firmar.</h1>
        <p class="lead">
          Sube un contrato o pega una cláusula. LexCheck IA identifica riesgos frecuentes,
          señala puntos críticos y propone una redacción más segura para revisión profesional.
        </p>
        <div class="benefits">
          <div class="benefit"><strong>Menos trabajo mecánico</strong><span>Detecta fechas, renovaciones, penalidades y datos sensibles sin revisar línea por línea.</span></div>
          <div class="benefit"><strong>Riesgos visibles</strong><span>Clasifica alertas por nivel alto, medio o bajo para priorizar la negociación.</span></div>
          <div class="benefit"><strong>Control de vigencia</strong><span>Marca renovaciones automáticas y vencimientos para evitar obligaciones no deseadas.</span></div>
          <div class="benefit"><strong>Contacto experto</strong><span>Al terminar la auditoría puedes solicitar ayuda de abogadas según la materia detectada.</span></div>
        </div>
      </div>

      <aside class="upload-panel">
        <h2 class="panel-title">Analizar contrato</h2>
        <p class="panel-copy">Puedes subir un archivo o pegar texto. Para PDF/Word esta demo revisa el nombre y genera una auditoría modelo; con texto pegado analiza el contenido.</p>

        <div class="input-section">
          <h3 class="field-title">1. Archivo</h3>
          <p class="field-help">Sube el documento si lo tienes en TXT, PDF, DOC o DOCX.</p>
          <label class="dropzone" id="dropzone">
            <input id="fileInput" type="file" accept=".txt,.pdf,.doc,.docx" />
            <span>
              <span class="upload-icon" aria-hidden="true">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                  <path d="M12 15V4m0 0 4 4m-4-4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M5 15v3a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </span>
              <b id="fileName">Arrastra o selecciona un contrato</b>
              <small>Formatos: TXT, PDF, DOC, DOCX</small>
            </span>
          </label>
        </div>

        <div class="input-section">
          <h3 class="field-title">2. Texto del contrato</h3>
          <p class="field-help">Pega el contrato completo o las cláusulas que quieras revisar. Mientras más texto ingreses, más completa será la auditoría.</p>
          <textarea id="contractText" placeholder="Ejemplo: El contrato se renovará automáticamente por períodos iguales..."></textarea>
        </div>

        <div class="input-section">
          <h3 class="field-title">3. Objetivo</h3>
          <p class="field-help">Explica qué quieres lograr para revisar si el contrato realmente permite cumplir esa finalidad.</p>
          <textarea class="purpose-textarea" id="purposeText" placeholder="Ejemplo: quiero alquilar un local por un año sin renovación automática y con opción de terminar si el propietario incumple."></textarea>
        </div>

        <div class="actions">
          <button class="primary" id="analyzeBtn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="m21 21-4.3-4.3M10.8 18a7.2 7.2 0 1 1 0-14.4 7.2 7.2 0 0 1 0 14.4Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Auditar ahora
          </button>
          <button class="secondary" id="demoBtn">Cargar ejemplo</button>
        </div>
        <p class="footer-note">Demo académica: no constituye asesoría legal. La revisión final siempre debe hacerla una abogada o abogado.</p>
      </aside>
    </section>

    <section class="dashboard">
      <aside class="results-panel">
        <div class="score">
          <div class="ring"><span id="scoreValue">--</span></div>
          <div>
            <div class="risk-label">Índice de riesgo</div>
            <h2 class="risk-title" id="riskTitle">Sin analizar</h2>
            <p class="risk-copy" id="riskCopy">Carga un contrato para generar un diagnóstico preliminar.</p>
          </div>
        </div>
        <div class="metrics">
          <div class="metric"><b id="highCount">0</b><span>Riesgos altos</span></div>
          <div class="metric"><b id="mediumCount">0</b><span>Riesgos medios</span></div>
          <div class="metric"><b id="lowCount">0</b><span>Observaciones</span></div>
        </div>
      </aside>

      <section class="clause-panel">
        <div class="toolbar">
          <div>
            <h2 class="panel-title">Hallazgos de auditoría</h2>
            <p class="panel-copy" style="margin:0">Riesgos detectados y sugerencias de mejora.</p>
          </div>
          <div class="tabs">
            <button class="tab active" data-filter="all">Todo</button>
            <button class="tab" data-filter="high">Alto</button>
            <button class="tab" data-filter="medium">Medio</button>
            <button class="tab" data-filter="low">Bajo</button>
          </div>
        </div>
        <div class="list" id="findings">
          <div class="empty">Todavía no hay hallazgos. Ejecuta una auditoría para ver el informe.</div>
        </div>
      </section>
    </section>

    <section class="lawyer-panel" id="lawyerPanel">
      <h2 class="panel-title">Contacta a especialistas en derecho civil</h2>
      <p class="panel-copy">Estas opciones permanecen disponibles para que puedas solicitar una revisión profesional de contratos civiles o recibir orientación sobre una posible controversia procesal civil.</p>

      <div class="lawyer-list">
        <article class="lawyer-card">
          <h3>Dra. Camila Rojas</h3>
          <p>Especialista en contratos civiles: compraventa, arrendamiento, prestación de servicios, mutuo, obligaciones y revisión antes de firma.</p>
          <div class="lawyer-meta">
            <span>Contratos civiles</span>
            <span>Revisión preventiva</span>
            <span>Atención virtual</span>
          </div>
          <div class="lawyer-actions">
            <a class="contact-link primary" href="https://wa.me/51999999111?text=Hola%2C%20quiero%20una%20revision%20de%20un%20contrato%20civil." target="_blank" rel="noopener">WhatsApp</a>
            <a class="contact-link secondary" href="mailto:camila.rojas@example.com?subject=Consulta%20sobre%20contrato%20civil">Correo</a>
          </div>
        </article>

        <article class="lawyer-card">
          <h3>Dra. Valeria Medina</h3>
          <p>Especialista en derecho civil patrimonial: obligaciones, penalidades, garantías, responsabilidad civil e indemnizaciones.</p>
          <div class="lawyer-meta">
            <span>Derecho civil patrimonial</span>
            <span>Penalidades</span>
            <span>Garantías</span>
          </div>
          <div class="lawyer-actions">
            <a class="contact-link primary" href="https://wa.me/51999999222?text=Hola%2C%20necesito%20asesoria%20sobre%20obligaciones%20o%20penalidades%20en%20un%20contrato." target="_blank" rel="noopener">WhatsApp</a>
            <a class="contact-link secondary" href="mailto:valeria.medina@example.com?subject=Consulta%20civil%20patrimonial">Correo</a>
          </div>
        </article>

        <article class="lawyer-card">
          <h3>Dra. Luciana Torres</h3>
          <p>Especialista en procesal civil: controversias contractuales, conciliación, competencia, jurisdicción y estrategia ante incumplimientos.</p>
          <div class="lawyer-meta">
            <span>Procesal civil</span>
            <span>Controversias</span>
            <span>Conciliación</span>
          </div>
          <div class="lawyer-actions">
            <a class="contact-link primary" href="https://wa.me/51999999333?text=Hola%2C%20quiero%20orientacion%20sobre%20una%20controversia%20contractual%20civil." target="_blank" rel="noopener">WhatsApp</a>
            <a class="contact-link secondary" href="mailto:luciana.torres@example.com?subject=Consulta%20procesal%20civil">Correo</a>
          </div>
        </article>
      </div>
      <p class="footer-note">Los nombres, correos y teléfonos son datos de ejemplo. Puedes reemplazarlos por contactos reales cuando tengas la información definitiva.</p>
    </section>
  </main>

  <section class="feedback-float" id="feedbackFloat" aria-live="polite">
    <div class="feedback-head">
      <div>
        <h2>Tu experiencia</h2>
        <p>Cuéntanos qué tan útil fue la página y qué podríamos mejorar.</p>
      </div>
      <button class="icon-button" id="feedbackClose" type="button" aria-label="Cerrar formulario de satisfacción">×</button>
    </div>

    <div class="feedback-field">
      <label for="satisfactionLevel">Nivel de satisfacción</label>
      <select id="satisfactionLevel">
        <option value="Muy satisfecha/o">Muy satisfecha/o</option>
        <option value="Satisfecha/o">Satisfecha/o</option>
        <option value="Regular">Regular</option>
        <option value="Poco satisfecha/o">Poco satisfecha/o</option>
      </select>
    </div>

    <div class="feedback-field">
      <label for="improvementText">Sugerencias de mejora</label>
      <textarea id="improvementText" placeholder="Escribe qué te gustó, qué fue confuso o qué agregarías."></textarea>
    </div>

    <div class="feedback-actions">
      <a class="contact-link primary" id="feedbackSend" href="mailto:lucianacastro1304.com?subject=Opinión%20sobre%20LexCheck%20IA">Enviar opinión</a>
      <button class="secondary" id="feedbackLater" type="button">Después</button>
    </div>
  </section>

  <script>
    const fileInput = document.getElementById("fileInput");
    const fileName = document.getElementById("fileName");
    const dropzone = document.getElementById("dropzone");
    const contractText = document.getElementById("contractText");
    const purposeText = document.getElementById("purposeText");
    const findingsEl = document.getElementById("findings");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const demoBtn = document.getElementById("demoBtn");
    const tabs = document.querySelectorAll(".tab");
    const feedbackFloat = document.getElementById("feedbackFloat");
    const feedbackClose = document.getElementById("feedbackClose");
    const feedbackLater = document.getElementById("feedbackLater");
    const feedbackSend = document.getElementById("feedbackSend");
    const satisfactionLevel = document.getElementById("satisfactionLevel");
    const improvementText = document.getElementById("improvementText");

    let lastFindings = [];
    let activeFilter = "all";
    const feedbackEmail = "lucianacastro1304.com";

    const rules = [
      {
        level: "high",
        title: "Renovación automática sin aviso suficiente",
        terms: ["renovacion automatica", "renovara automaticamente", "prorroga automatica"],
        detail: "El contrato podría extenderse sin una confirmación expresa, generando obligaciones futuras no deseadas.",
        suggestion: "Agregar aviso previo mínimo de 30 a 60 días y exigir aceptación escrita para renovar.",
        area: "Contratos civiles"
      },
      {
        level: "high",
        title: "Penalidad desproporcionada",
        terms: ["penalidad", "multa", "clausula penal", "sancion"],
        detail: "La sanción económica puede ser excesiva si no se vincula al daño real o a un límite razonable.",
        suggestion: "Limitar la penalidad a un porcentaje definido del valor del contrato y permitir prueba del daño.",
        area: "Contratos civiles"
      },
      {
        level: "high",
        title: "Tratamiento de datos personales insuficiente",
        terms: ["datos personales", "proteccion de datos", "habeas data", "confidencialidad de datos"],
        detail: "Falta revisar base legal, finalidad, autorización, medidas de seguridad y responsables del tratamiento.",
        suggestion: "Incluir autorización, finalidad específica, encargado/responsable y procedimiento para derechos del titular.",
        area: "Contratos civiles"
      },
      {
        level: "medium",
        title: "Terminación unilateral amplia",
        terms: ["terminar unilateralmente", "terminacion unilateral", "sin justa causa"],
        detail: "Una parte podría finalizar el contrato sin equilibrar preavisos, pagos pendientes o compensaciones.",
        suggestion: "Definir causales, preaviso, liquidación de obligaciones y efectos posteriores a la terminación.",
        area: "Contratos civiles"
      },
      {
        level: "medium",
        title: "Jurisdicción o ley aplicable poco clara",
        terms: ["jurisdiccion", "ley aplicable", "tribunales", "arbitraje"],
        detail: "La falta de foro o mecanismo de solución de controversias puede aumentar costos y demoras.",
        suggestion: "Precisar ciudad, autoridad competente, ley aplicable y etapa previa de arreglo directo.",
        area: "Procesal civil"
      },
      {
        level: "medium",
        title: "Obligaciones de confidencialidad incompletas",
        terms: ["confidencial", "confidencialidad", "secreto"],
        detail: "La cláusula debe indicar duración, excepciones, personas autorizadas y consecuencias por incumplimiento.",
        suggestion: "Agregar alcance, exclusiones, plazo posterior al contrato y deber de devolución o destrucción de información.",
        area: "Contratos civiles"
      },
      {
        level: "low",
        title: "Fechas o plazos requieren validacion",
        terms: ["fecha", "plazo", "vigencia", "vencimiento"],
        detail: "Conviene confirmar que fechas, vigencia y entregables coincidan con la negociación real.",
        suggestion: "Crear una matriz de fechas criticas con vencimiento, aviso previo y responsable interno.",
        area: "Contratos civiles"
      },
      {
        level: "low",
        title: "Redacción general ambigua",
        terms: ["a criterio", "razonable", "cuando corresponda", "entre otros"],
        detail: "Expresiones abiertas pueden permitir interpretaciones distintas durante la ejecución.",
        suggestion: "Reemplazar fórmulas abiertas por criterios medibles, plazos concretos y responsables identificados.",
        area: "Derecho civil patrimonial"
      }
    ];

    const purposeRules = [
      {
        intentTerms: ["alquilar", "arrendar", "arrendamiento", "local", "vivienda", "inmueble"],
        requiredTerms: ["arrendamiento", "arrendador", "arrendatario", "renta", "merced conductiva", "inmueble", "plazo"],
        title: "Finalidad de arrendamiento no completamente cubierta",
        detail: "La finalidad indicada parece relacionada con un arrendamiento. Conviene que el contrato identifique bien el inmueble, renta, plazo, obligaciones de uso, devolución y causales de resolución.",
        suggestion: "Verificar que el contrato incluya descripción del bien, monto y forma de pago, plazo, garantía, estado de entrega y reglas de terminación.",
        area: "Contratos civiles"
      },
      {
        intentTerms: ["comprar", "vender", "compraventa", "propiedad", "transferir"],
        requiredTerms: ["compraventa", "vendedor", "comprador", "precio", "bien", "transferencia", "entrega"],
        title: "Finalidad de compraventa requiere cláusulas esenciales",
        detail: "La finalidad indicada parece vinculada a una compraventa. El contrato debe dejar claro el bien, precio, forma de pago, entrega, saneamiento y transferencia.",
        suggestion: "Revisar que existan cláusulas sobre identificación del bien, precio total, cronograma de pago, entrega, saneamiento y consecuencias por incumplimiento.",
        area: "Contratos civiles"
      },
      {
        intentTerms: ["servicio", "servicios", "contratar", "proveedor", "trabajo", "entregable"],
        requiredTerms: ["servicio", "prestacion", "entregable", "plazo", "pago", "obligaciones", "conformidad"],
        title: "Finalidad de prestación de servicios necesita mayor precisión",
        detail: "La finalidad indicada parece relacionada con servicios. El contrato debe definir con precisión el servicio, entregables, pagos, plazos y criterios de conformidad.",
        suggestion: "Agregar alcance del servicio, fechas de entrega, forma de aprobación, pagos, penalidades razonables y causales de resolución.",
        area: "Contratos civiles"
      },
      {
        intentTerms: ["prestar dinero", "prestamo", "mutuo", "deuda", "devolver dinero"],
        requiredTerms: ["mutuo", "prestamo", "deudor", "acreedor", "monto", "interes", "cuotas", "vencimiento"],
        title: "Finalidad de préstamo o mutuo requiere condiciones claras",
        detail: "La finalidad indicada parece relacionada con un préstamo de dinero. Deben quedar claros monto, intereses, fecha de devolución, cuotas y consecuencias por mora.",
        suggestion: "Verificar monto, moneda, cronograma de pago, intereses, mora, garantías y mecanismo para exigir el cumplimiento.",
        area: "Derecho civil patrimonial"
      },
      {
        intentTerms: ["evitar juicio", "demandar", "incumplimiento", "conciliar", "controversia", "problema legal"],
        requiredTerms: ["conciliacion", "jurisdiccion", "competencia", "domicilio", "incumplimiento", "resolucion"],
        title: "Finalidad preventiva ante conflicto civil",
        detail: "La finalidad indicada menciona un posible conflicto. Conviene que el contrato prevea comunicaciones, solución de controversias, competencia y efectos del incumplimiento.",
        suggestion: "Incluir domicilio contractual, forma de notificación, etapa de conciliación, competencia judicial y reglas para resolver el contrato.",
        area: "Procesal civil"
      }
    ];

    const demoText = `Contrato de prestación de servicios con renovación automática por períodos iguales.
La parte contratante podrá terminar unilateralmente el acuerdo sin justa causa.
Se pacta penalidad del 40% del valor total por cualquier incumplimiento.
El proveedor tratará datos personales de clientes y empleados.
La información confidencial deberá mantenerse en secreto durante la vigencia del contrato.
La jurisdicción será definida posteriormente por las partes.`;

    const demoPurpose = "Quiero contratar un servicio por un plazo definido, evitar renovación automática y poder terminar si la otra parte incumple.";

    fileInput.addEventListener("change", async () => {
      const file = fileInput.files[0];
      if (!file) return;
      fileName.textContent = file.name;
      if (file.name.toLowerCase().endsWith(".txt")) {
        contractText.value = await file.text();
      } else {
        contractText.value = `Archivo cargado: ${file.name}. Demo preparada para auditar riesgos frecuentes de contratos PDF o Word.`;
      }
    });

    ["dragenter", "dragover"].forEach(eventName => {
      dropzone.addEventListener(eventName, event => {
        event.preventDefault();
        dropzone.classList.add("dragging");
      });
    });

    ["dragleave", "drop"].forEach(eventName => {
      dropzone.addEventListener(eventName, event => {
        event.preventDefault();
        dropzone.classList.remove("dragging");
      });
    });

    dropzone.addEventListener("drop", event => {
      const file = event.dataTransfer.files[0];
      if (!file) return;
      fileInput.files = event.dataTransfer.files;
      fileInput.dispatchEvent(new Event("change"));
    });

    demoBtn.addEventListener("click", () => {
      contractText.value = demoText;
      purposeText.value = demoPurpose;
      fileName.textContent = "Contrato de servicios - ejemplo";
      analyze();
    });

    analyzeBtn.addEventListener("click", analyze);

    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        tabs.forEach(item => item.classList.remove("active"));
        tab.classList.add("active");
        activeFilter = tab.dataset.filter;
        renderFindings();
      });
    });

    feedbackClose.addEventListener("click", hideFeedback);
    feedbackLater.addEventListener("click", hideFeedback);
    satisfactionLevel.addEventListener("change", updateFeedbackEmail);
    improvementText.addEventListener("input", updateFeedbackEmail);

    function analyze() {
      const text = normalize(contractText.value || "");
      const purpose = normalize(purposeText.value || "");
      const hasRealText = text.trim().length > 12;
      const matched = rules.filter(rule => rule.terms.some(term => text.includes(normalize(term))));
      const purposeFindings = analyzePurpose(text, purpose);

      if (!hasRealText) {
        lastFindings = [
          {
            level: "medium",
            title: "No se encontró texto suficiente",
            detail: "Para una auditoría más precisa, pega cláusulas del contrato o carga un archivo TXT.",
            suggestion: "En una versión productiva, el sistema extraería texto de PDF y Word desde el servidor.",
            area: "Derecho civil patrimonial"
          }
        ];
      } else {
        const combinedFindings = [...matched, ...purposeFindings];
        lastFindings = combinedFindings.length ? combinedFindings : [
          {
            level: "low",
            title: "Sin alertas críticas en la muestra",
            detail: "No se detectaron patrones de riesgo frecuentes en el texto revisado.",
            suggestion: "Completar la revisión con obligaciones de pago, terminación, datos personales, garantías y anexos.",
            area: "Contratos civiles"
          }
        ];
      }

      updateScore();
      renderFindings();
      showFeedback();
    }

    function analyzePurpose(contractValue, purposeValue) {
      if (purposeValue.trim().length < 12) return [];

      const findings = [];
      const matchedPurposeRules = purposeRules.filter(rule =>
        rule.intentTerms.some(term => purposeValue.includes(normalize(term)))
      );

      matchedPurposeRules.forEach(rule => {
        const coveredTerms = rule.requiredTerms.filter(term => contractValue.includes(normalize(term)));
        const coverage = coveredTerms.length / rule.requiredTerms.length;

        if (coverage < 0.35) {
          findings.push({
            level: "high",
            title: rule.title,
            detail: rule.detail,
            suggestion: rule.suggestion,
            area: rule.area
          });
        } else if (coverage < 0.65) {
          findings.push({
            level: "medium",
            title: "La finalidad está parcialmente cubierta",
            detail: `El contrato parece relacionarse con lo que quieres hacer, pero no cubre suficientes elementos clave para ${rule.title.toLowerCase()}.`,
            suggestion: rule.suggestion,
            area: rule.area
          });
        } else {
          findings.push({
            level: "low",
            title: "Finalidad declarada aparentemente compatible",
            detail: "El contrato contiene varios elementos relacionados con la finalidad que indicaste. Aun así, conviene revisar que las cláusulas sean suficientes y no contradigan tu objetivo.",
            suggestion: "Confirmar con una especialista que el texto final permita cumplir tu finalidad concreta antes de firmar.",
            area: rule.area
          });
        }
      });

      if (!matchedPurposeRules.length) {
        findings.push({
          level: "medium",
          title: "Finalidad del contrato requiere revisión manual",
          detail: "La app no pudo asociar claramente tu objetivo con una categoría civil específica. Puede tratarse de una finalidad especial o estar redactada de forma muy abierta.",
          suggestion: "Explica la finalidad con más detalle: qué quieres recibir, qué obligación asumirá la otra parte, plazo, pago, riesgos y qué pasaría si alguien incumple.",
          area: "Contratos civiles"
        });
      }

      return findings;
    }

    function normalize(value) {
      return value.toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
    }

    function updateScore() {
      const high = lastFindings.filter(item => item.level === "high").length;
      const medium = lastFindings.filter(item => item.level === "medium").length;
      const low = lastFindings.filter(item => item.level === "low").length;
      const score = Math.min(99, high * 28 + medium * 15 + low * 6);

      document.getElementById("scoreValue").textContent = score;
      document.getElementById("highCount").textContent = high;
      document.getElementById("mediumCount").textContent = medium;
      document.getElementById("lowCount").textContent = low;

      const title = document.getElementById("riskTitle");
      const copy = document.getElementById("riskCopy");
      if (score >= 55) {
        title.textContent = "Riesgo alto";
        copy.textContent = "Se recomienda revisión legal prioritaria antes de firma o negociación.";
      } else if (score >= 20) {
        title.textContent = "Riesgo medio";
        copy.textContent = "Hay puntos que conviene ajustar para reducir ambigüedad y exposición.";
      } else {
        title.textContent = "Riesgo bajo";
        copy.textContent = "No aparecen alertas graves en la muestra, pero falta revisión profesional completa.";
      }
    }

    function renderFindings() {
      const visible = activeFilter === "all"
        ? lastFindings
        : lastFindings.filter(item => item.level === activeFilter);

      if (!visible.length) {
        findingsEl.innerHTML = '<div class="empty">No hay hallazgos para este filtro.</div>';
        return;
      }

      findingsEl.innerHTML = visible.map(item => `
        <article class="finding ${item.level}">
          <div class="finding-head">
            <h3>${item.title}</h3>
            <span class="tag">${labelFor(item.level)}</span>
          </div>
          <p>${item.detail}</p>
          <div class="suggestion"><strong>Sugerencia:</strong> ${item.suggestion}</div>
        </article>
      `).join("");
    }

    function showFeedback() {
      updateFeedbackEmail();
      window.setTimeout(() => feedbackFloat.classList.add("visible"), 650);
    }

    function hideFeedback() {
      feedbackFloat.classList.remove("visible");
    }

    function updateFeedbackEmail() {
      const score = document.getElementById("scoreValue").textContent;
      const riskTitle = document.getElementById("riskTitle").textContent;
      const body = [
        "Hola, quiero compartir mi opinión sobre LexCheck IA.",
        "",
        `Nivel de satisfacción: ${satisfactionLevel.value}`,
        `Resultado obtenido: ${riskTitle} (${score})`,
        "",
        "Sugerencias:",
        improvementText.value || "Sin comentario adicional."
      ].join("\n");

      feedbackSend.href = `mailto:${feedbackEmail}?subject=${encodeURIComponent("Opinión sobre LexCheck IA")}&body=${encodeURIComponent(body)}`;
    }

    function labelFor(level) {
      if (level === "high") return "Alto";
      if (level === "medium") return "Medio";
      return "Bajo";
    }
  </script>
</body>
</html>"""


class LexCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def log_message(self, format, *args):
        return


def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), LexCheckHandler)
    print(f"LexCheck IA listo en http://localhost:{PORT}")
    Timer(1, open_browser).start()
    server.serve_forever()
