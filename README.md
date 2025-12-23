# Estrategia de Pricing y Rentabilidad: Rent-of-Car 2025
### Análisis de gestión de ingresos y optimización de flotas

**Analista:** Julio Lagos  
**Stack Técnico:** `Python` | `SQL (SQLite3)` | `Pandas` | `Seaborn` | `Matplotlib`

---

> **Resumen del Proyecto:** > Auditoría integral de datos para identificar fugas de ingresos por sub-valoración de flota y optimización de márgenes mediante estrategias de precios dinámicos.

## Hallazgos Estratégicos (Insights)
* **Ineficiencia del Descuento Estacional:** El uso de un multiplicador de **0.80** en temporada baja es contraproducente. La demanda se mantiene estable (70-80% de ocupación), lo que demuestra que se está sacrificando margen innecesariamente.
* **Crisis de Rentabilidad en Económicos:** Se identificó un **RevPAR crítico de <$2 USD** en meses valle para la categoría económica, situándose por debajo del costo operativo estimado.
* **Escasez Estructural en Camionetas (SUV):** Esta categoría presenta agotamiento de inventario (más de 12 días de escasez en abril), incluso fuera de temporada alta, sugiriendo una demanda subestimada o inventario insuficiente.

## Visualizaciones Incluidas
El análisis se apoya en tres ejes visuales desarrollados con Seaborn y Matplotlib:
1. **Ingresos vs. Ocupación:** Análisis de la inelasticidad de la demanda mensual.
2. **Evolución del RevPAR:** Evaluación de la rentabilidad diaria neta por categoría.
3. **Mapa de Calor de Escasez:** Localización de quiebres de stock (Stockouts) y días críticos.

## Instalación y Uso
Para replicar este análisis localmente:

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/Azoth17/car-rental-pricing-analysis.git](https://github.com/Azoth17/car-rental-pricing-analysis.git)
   ```


Asegurarse de tener el archivo de base de datos .db en la carpeta raíz de los scripts.

Instalar las dependencias:

```bash
pip install pandas seaborn matplotlib
```

Ejecutar el archivo .ipynb en Jupyter Notebook o VS Code.

Conclusión de Negocio
La mayor oportunidad de crecimiento no reside en la expansión física de la flota, sino en la transición hacia un modelo de Precios Dinámicos (Yield Management). Implementar un multiplicador basado en disponibilidad permitiría capturar el valor de los clientes de último minuto cuando el inventario es escaso, incrementando el margen neto sin inversión adicional en activos.

Desarrollado por Julio Lagos | [Linkedin](https://www.linkedin.com/in/julio-lagos-3256b4216/)
