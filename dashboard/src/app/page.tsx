"use client";

import { useEffect, useState } from "react";

type Summary = {
  total_claims: number;
  pending_claims: number;
  avg_discrepancy: number;
};

type AuditItem = {
  claim_id: string;
  reason: string;
  discrepancy?: number;
  ela_score?: number;
};

type Cluster = {
  lat_bin: number;
  lon_bin: number;
  points: number;
};

type RegionReport = {
  district: string;
  village: string;
  image_reports: number;
  avg_discrepancy: number | null;
};

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Page() {
  const [token, setToken] = useState("");
  const [summary, setSummary] = useState<Summary>({
    total_claims: 0,
    pending_claims: 0,
    avg_discrepancy: 0,
  });
  const [queue, setQueue] = useState<AuditItem[]>([]);
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [regions, setRegions] = useState<RegionReport[]>([]);

  async function loadData(currentToken: string) {
    if (!currentToken) {
      return;
    }
    const headers = { Authorization: `Bearer ${currentToken}` };

    const [summaryRes, queueRes, clustersRes, regionsRes] = await Promise.all([
      fetch(`${API}/v1/dashboard/summary`, { headers }),
      fetch(`${API}/v1/audit/queue`, { headers }),
      fetch(`${API}/v1/dashboard/clusters`, { headers }),
      fetch(`${API}/v1/dashboard/regions`, { headers }),
    ]);

    if (summaryRes.ok) {
      setSummary(await summaryRes.json());
    }
    if (queueRes.ok) {
      const payload = await queueRes.json();
      setQueue(payload.items ?? []);
    }
    if (clustersRes.ok) {
      const payload = await clustersRes.json();
      setClusters(payload.items ?? []);
    }
    if (regionsRes.ok) {
      const payload = await regionsRes.json();
      setRegions(payload.items ?? []);
    }
  }

  useEffect(() => {
    const stored = localStorage.getItem("cropic_token") || "";
    setToken(stored);
    if (stored) {
      loadData(stored);
    }
  }, []);

  function saveToken() {
    localStorage.setItem("cropic_token", token);
    loadData(token);
  }

  const top = queue[0];

  return (
    <div className="layout">
      <aside className="nav">
        <div className="panel">
          <strong>CROPIC Command</strong>
        </div>
        <div className="panel">Claims</div>
        <div className="panel">Farm Maps</div>
        <div className="panel">Fraud Queue</div>
        <div className="panel">
          <input
            style={{ width: "100%" }}
            placeholder="JWT token"
            value={token}
            onChange={(e) => setToken(e.target.value)}
          />
          <button style={{ marginTop: 8, width: "100%" }} onClick={saveToken}>
            Load Live Data
          </button>
        </div>
      </aside>

      <main className="main">
        <section className="kpis">
          <article className="panel kpi">
            <span>Total Claims</span>
            <strong>{summary.total_claims}</strong>
          </article>
          <article className="panel kpi">
            <span>Pending</span>
            <strong>{summary.pending_claims}</strong>
          </article>
          <article className="panel kpi">
            <span>Avg Discrepancy</span>
            <strong>{(summary.avg_discrepancy * 100).toFixed(1)}%</strong>
          </article>
        </section>
        <section className="panel map">
          <h3>NDVI + Stress Map</h3>
          <p>Top cluster bins from live backend data:</p>
          <ul>
            {clusters.slice(0, 5).map((c, idx) => (
              <li key={idx}>
                ({c.lat_bin}, {c.lon_bin}) - {c.points} reports
              </li>
            ))}
          </ul>
        </section>
        <section className="panel">
          <h3>District/Village Stress Reports</h3>
          <ul>
            {regions.slice(0, 6).map((r, idx) => (
              <li key={idx}>
                {r.district}/{r.village} - {r.image_reports} reports, avg discrepancy{" "}
                {r.avg_discrepancy ?? 0}
              </li>
            ))}
          </ul>
        </section>
      </main>

      <aside className="aside">
        <section className="panel">
          <h3>Flagged Claim</h3>
          <p>Claim ID: {top?.claim_id || "-"}</p>
          <p>Discrepancy: {top?.discrepancy?.toFixed(2) ?? "-"}</p>
          <p>Tamper ELA: {top?.ela_score?.toFixed(2) ?? "-"}</p>
          <p style={{ color: "#c74636", fontWeight: 700 }}>{top ? top.reason : "No active flags"}</p>
        </section>
        <section className="panel">
          <h3>Fraud Alerts</h3>
          <p>{queue.length} alerts in queue</p>
        </section>
      </aside>
    </div>
  );
}
