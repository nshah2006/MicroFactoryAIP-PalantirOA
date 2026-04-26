"use client";
import { useEffect, useState } from "react";
import { fetchAudit, fetchGraph, fetchSummary, fetchWorkOrders, generateRecovery, triggerDisruption } from "@/lib/api";
import { useCommandCenterStore } from "@/stores/command-center-store";

export default function CommandCenter() {
  const [summary, setSummary] = useState<any>();
  const [workOrders, setWorkOrders] = useState<any[]>([]);
  const [audit, setAudit] = useState<any[]>([]);
  const [recovery, setRecovery] = useState<any>(null);
  const [banner, setBanner] = useState(false);
  const [graph, setGraph] = useState<any>({ nodes: [], edges: [] });
  const { role, setRole } = useCommandCenterStore();

  const load = async () => {
    setSummary(await fetchSummary());
    setWorkOrders(await fetchWorkOrders());
    setAudit(await fetchAudit());
    setGraph(await fetchGraph());
  };
  useEffect(() => { load(); }, []);

  return <div className="p-4 space-y-4">
    <header className="flex justify-between border border-border bg-panel p-3 rounded">
      <h1 className="font-semibold">MicroFactory Command Center</h1>
      <select className="bg-elevated border border-border px-2 py-1" value={role} onChange={e => setRole(e.target.value as any)}>
        <option>Operator</option><option>Manufacturing Engineer</option><option>Operations Manager</option>
      </select>
    </header>
    {summary && <div className="grid grid-cols-5 gap-2">{Object.entries(summary).slice(0,5).map(([k,v])=><div key={k} className="bg-panel border border-border p-3 rounded"><div className="text-xs text-muted uppercase">{k}</div><div className="text-xl">{String(v)}</div></div>)}</div>}
    {banner && <div className="bg-amber-950 border border-warning p-3 rounded">Supplier delay detected: Northline Components delayed DRV-042 by 4 days. 7 work orders blocked. 3 builds at risk.</div>}
    <div className="flex gap-2">
      <button onClick={async()=>{await triggerDisruption(); setBanner(true); await load();}} className="bg-critical px-3 py-2 rounded">Trigger Demo Disruption</button>
      <button onClick={async()=>{setRecovery(await generateRecovery()); await load();}} className="bg-primary px-3 py-2 rounded">Generate Recovery Plan</button>
      <button onClick={load} className="bg-panel border border-border px-3 py-2 rounded">Reset View</button>
    </div>
    <div className="grid grid-cols-3 gap-3">
      <div className="col-span-2 bg-panel border border-border rounded p-3"><h2 className="mb-2">Ontology Graph</h2><pre className="text-xs text-muted overflow-auto h-56">{JSON.stringify(graph,null,2)}</pre></div>
      <div className="bg-panel border border-border rounded p-3"><h2>Recovery Panel</h2>{recovery ? <pre className="text-xs text-muted">{JSON.stringify(recovery,null,2)}</pre> : <p className="text-muted text-sm">Generate recovery plan to view actions.</p>}</div>
    </div>
    <div className="grid grid-cols-2 gap-3">
      <div className="bg-panel border border-border rounded p-3"><h2>Work Orders</h2><table className="w-full text-sm"><thead><tr><th className="text-left">WO</th><th>Status</th><th>Part</th></tr></thead><tbody>{workOrders.slice(0,15).map((w)=><tr key={w.work_order_code}><td>{w.work_order_code}</td><td>{w.status}</td><td>{w.required_part_code}</td></tr>)}</tbody></table></div>
      <div className="bg-panel border border-border rounded p-3"><h2>Audit Timeline</h2><ul className="text-sm">{audit.map((a,i)=><li key={i}>{a.time} · {a.actor} · {a.message}</li>)}</ul></div>
    </div>
  </div>
}
