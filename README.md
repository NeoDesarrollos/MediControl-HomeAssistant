# MediControl - Pastillero Domótico

![MediControl](https://neodesarrollos.com/MediControl.png)

Para poder usar esta integración es necesario contar con el equipo **MediControl**.

MediControl es un dispensador inteligente de medicamentos diseñado para facilitar el cumplimiento de tratamientos, tanto crónicos como temporales, aportando seguridad, autonomía y tranquilidad al usuario y a su familia.

Dispone de 30 compartimentos y permite configurar hasta 6 horarios diferentes por día, dispensando automáticamente la medicación en el momento programado mediante un sistema motorizado y una alerta sonora. Su funcionamiento es completamente autónomo, por lo que no necesita conexión a Internet para realizar las dispensaciones.

La configuración se realiza desde una interfaz web muy sencilla e intuitiva, accesible desde cualquier móvil, tablet o ordenador. Además, puede conectarse a una red WiFi e integrarse con Home Assistant, permitiendo crear automatizaciones y recibir notificaciones mediante Alexa o Google Home.

Su pantalla integrada muestra en todo momento información relevante como la hora actual, próxima toma, estado del equipo y otros datos del tratamiento. También incorpora un asistente de configuración que facilita la carga de los medicamentos y ayuda a conocer el estado del pastillero en todo momento.

Entre sus funciones destaca la posibilidad de calcular automáticamente hasta qué fecha alcanzará la medicación cargada, permitiendo planificar con antelación la compra o reposición de los medicamentos.

Su diseño es robusto, elegante y discreto, ideal para cualquier hogar, residencia o consulta médica. Funciona mediante alimentación USB-C e incluye su correspondiente cargador.

Características principales:

✅ 30 compartimentos de almacenamiento.
✅ Hasta 6 horarios programables por día.
✅ Dispensación automática con aviso sonoro.
✅ Funcionamiento autónomo, sin necesidad de Internet.
✅ Configuración desde navegador web.
✅ Compatible con WiFi y Home Assistant (MQTT).
✅ Integración con Alexa y Google Home mediante automatizaciones.
✅ Pantalla informativa con estado del tratamiento.
✅ Cálculo de la duración de la medicación cargada.
✅ Alimentación mediante USB-C con cargador incluido.

MediControl convierte la toma diaria de medicamentos en un proceso simple, seguro y automatizado, ayudando a evitar olvidos y mejorando la adherencia a los tratamientos.

Para más información y compra del equipo, visitá: [https://neodesarrollos.com](https://neodesarrollos.com)

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Compatible-41BDF5?logo=homeassistant&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-Integrado-660066?logo=mqtt&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-Estable-16A34A)

Integracion oficial para conectar MediControl con Home Assistant de forma simple y estable.

**Creador:** Jorge Piovano  
**Empresa:** NeoDesarrollos.com

## Que hace esta integracion

- Lee el estado del equipo MediControl desde MQTT.
- Crea sensores listos para usar en Home Assistant.
- Evita que el usuario tenga que editar `configuration.yaml`.

## Sensores principales

- Proxima toma (hora)
- Proxima toma (medicamentos)
- Dias restantes
- Compartimento actual
- Compartimentos maximos
- Compartimentos restantes

## Instalacion (usuario final)

1. Abrir HACS.
2. Ir a **Integrations**.
3. Agregar repositorio personalizado: `https://github.com/NeoDesarrollos/MediControl-HomeAssistant`.
4. Tipo: **Integration**.
5. Instalar **MediControl**.
6. Reiniciar Home Assistant.
7. Ir a **Configuracion > Dispositivos y servicios > Anadir integracion**.
8. Buscar **MediControl** y completar:
   - Nombre del dispositivo (default: `MediControl`)
   - Prefijo MQTT (default: `medicontrol`)

## Panel recomendado (copiar y pegar)

Cuando ya tengas el dispositivo funcionando, crea un dashboard o vista nueva y agrega una tarjeta en modo manual:

1. Ve a tu dashboard.
2. Pulsa **Editar dashboard**.
3. **Agregar tarjeta**.
4. Selecciona **Manual**.
5. Borra todo y pega el siguiente YAML.

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # MediControl
      **Proxima toma:** {{ states('sensor.medicontrol_proxima_toma_hora') }}
      **Medicamentos:** {{ states('sensor.medicontrol_proxima_toma_medicamentos') }}
      **Dias restantes:** {{ states('sensor.medicontrol_dias_restantes') }}

  - type: markdown
    title: Lista completa de horarios
    content: >-
      {% set detalle = states('sensor.medicontrol_horarios_y_medicamentos') %}
      {% if detalle in ['unknown', 'unavailable', 'Sin horarios'] %}
      Sin horarios cargados.
      {% else %}
      {% for row in detalle.split(' | ') %}
      - {{ row }}
      {% endfor %}
      {% endif %}

  - type: entities
    title: Estado del tratamiento
    entities:
      - entity: sensor.medicontrol_compartimento_actual
        name: Compartimento actual
      - entity: sensor.medicontrol_compartimentos_restantes
        name: Compartimentos restantes
      - entity: sensor.medicontrol_compartimentos_maximos
        name: Compartimentos maximos

  - type: entities
    title: Red del dispositivo
    entities:
      - entity: sensor.medicontrol_wifi
        name: WiFi conectada
        icon: mdi:wifi
      - entity: sensor.medicontrol_ip
        name: IP del equipo
        icon: mdi:ip-network

  - type: grid
    columns: 3
    square: false
    cards:
      - type: gauge
        entity: sensor.medicontrol_compartimento_actual
        name: Tomadas
        min: 0
        max: 30
        severity:
          green: 0
          yellow: 10
          red: 20
      - type: gauge
        entity: sensor.medicontrol_compartimentos_restantes
        name: Disponibles
        min: 0
        max: 30
        severity:
          red: 0
          yellow: 8
          green: 16
      - type: gauge
        entity: sensor.medicontrol_compartimentos_maximos
        name: Libres
        min: 0
        max: 30
        severity:
          green: 0
          yellow: 10
          red: 20
```

## Panel premium (opcional)

Si quieres un panel mas visual y moderno, puedes usar esta version premium.

### Requisitos premium

Instalar desde HACS (Frontend):

- `Mushroom`
- `Button Card`
- `Card Mod`

### Como usarlo

1. Ve a tu dashboard.
2. Pulsa **Editar dashboard**.
3. **Agregar tarjeta**.
4. Selecciona **Manual**.
5. Borra todo y pega este YAML.

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: MediControl
    subtitle: Panel premium

  - type: grid
    columns: 2
    square: false
    cards:
      - type: custom:mushroom-template-card
        primary: Proxima toma
        secondary: "{{ states('sensor.medicontrol_proxima_toma_hora') }}"
        icon: mdi:clock-outline
        icon_color: amber
      - type: custom:mushroom-template-card
        primary: Dias restantes
        secondary: "{{ states('sensor.medicontrol_dias_restantes') }} dias"
        icon: mdi:calendar-clock
        icon_color: teal

  - type: custom:mushroom-template-card
    primary: Medicamentos proximos
    secondary: "{{ states('sensor.medicontrol_proxima_toma_medicamentos') }}"
    multiline_secondary: true
    icon: mdi:pill
    icon_color: green

  - type: custom:mushroom-template-card
    primary: Lista completa por horario
    secondary: >-
      {% set detalle = states('sensor.medicontrol_horarios_y_medicamentos') %}
      {% if detalle in ['unknown', 'unavailable', 'Sin horarios'] %}
      Sin horarios cargados.
      {% else %}
      {{ detalle.replace(' | ', '\n') }}
      {% endif %}
    multiline_secondary: true
    icon: mdi:format-list-bulleted
    icon_color: blue

  - type: entities
    title: Red del dispositivo
    entities:
      - entity: sensor.medicontrol_wifi
        name: WiFi conectada
        icon: mdi:wifi
      - entity: sensor.medicontrol_ip
        name: IP del equipo
        icon: mdi:ip-network

  - type: custom:button-card
    name: ""
    show_name: false
    show_icon: false
    show_state: false
    styles:
      card:
        - padding: 10px 12px
        - border-radius: 18px
        - width: 100%
      custom_fields:
        body:
          - display: block
          - width: 100%
          - justify-self: stretch
          - align-self: stretch
    custom_fields:
      body: >-
        [[[ 
          const usados = Number(states['sensor.medicontrol_compartimento_actual']?.state || 0);
          const total = Number(states['sensor.medicontrol_compartimentos_maximos']?.state || 0);
          const libres = Math.max(31 - total, 0);
          const disponibles = Math.max(total - usados, 0);
          const dot = (color) => `<span style="width:14px;height:14px;border-radius:50%;border:1px solid rgba(0,0,0,.12);background:${color};"></span>`;
          const dots = [
            ...Array(Math.max(usados,0)).fill(dot('rgba(244,67,54,.45)')),
            ...Array(Math.max(disponibles,0)).fill(dot('rgb(76,175,80)')),
            ...Array(Math.max(libres,0)).fill(dot('rgba(158,158,158,.30)')),
          ];
          const grid = `<div style="display:grid;width:100%;grid-template-columns:repeat(10,minmax(0,1fr));gap:8px;justify-items:center;align-items:center;">${dots.join('')}</div>`;

          return `
            <div style="font-size:12px;line-height:1.5;">
              <div style="margin-top:2px;">${grid}</div>
              <div style="margin-top:8px;"><b>Resumen:</b> ${libres} libres | ${usados} tomados | ${disponibles} disponibles</div>
            </div>
          `;
        ]]]
```

> Nota: este panel premium es visual. La logica de datos sigue siendo la misma y depende de los sensores de MediControl.

## Importante sobre datos "No disponible"

Si ves sensores en "No disponible", revisa:

1. Que el equipo este conectado al broker MQTT.
2. Que el prefijo configurado en la integracion coincida (por defecto `medicontrol`).
3. Que exista trafico en `medicontrol/medicamentos`.
4. Reiniciar Home Assistant luego de instalar/actualizar la integracion.

Compatibilidad:
- Esta integracion acepta tanto claves nuevas (`proximoHora`, `proximoMedicamentos`) como claves anteriores (`proximo`, `lista`) para facilitar migraciones.

## Soporte

- Web: https://neodesarrollos.com
- Repositorio: https://github.com/NeoDesarrollos/MediControl-HomeAssistant
