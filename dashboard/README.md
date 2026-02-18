# Dashboard Scaffold

## Implemented
- Next.js app shell
- Three-column command-center layout
- KPI cards, map canvas placeholder, fraud/claim detail panel

## Next
- Bind APIs for claim stream, audit queue, and NDVI overlays
- Integrate map provider (Mapbox/Leaflet)
- Add filters and trend charts

## Live Data
- Set `NEXT_PUBLIC_API_URL` to backend URL (default `http://localhost:8000`).
- Generate JWT from backend `POST /v1/auth/token`.
- Paste token in dashboard sidebar and click `Load Live Data`.
