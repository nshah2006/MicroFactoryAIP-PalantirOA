const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

export async function fetchSummary() { return (await fetch(`${API}/dashboard/summary`)).json(); }
export async function fetchWorkOrders() { return (await fetch(`${API}/work-orders`)).json(); }
export async function fetchAudit() { return (await fetch(`${API}/audit`)).json(); }
export async function fetchGraph() { return (await fetch(`${API}/ontology/graph`)).json(); }

export async function triggerDisruption() {
  return (await fetch(`${API}/disruptions/supplier-delay`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ supplierName: "Northline Components", partCode: "DRV-042", delayDays: 4 }) })).json();
}

export async function generateRecovery() {
  return (await fetch(`${API}/recovery/generate`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ issueCode: "ISS-009" }) })).json();
}
