import React, { useMemo, useState } from "react";
import { api } from "./lib/api";

const sampleHint = `date,product_name,quantity_sold,price,revenue
2026-01-01,Atta 1kg,10,45,450`;

export default function App(){
  const [csvText,setCsvText]=useState("");
  const [lang,setLang]=useState("en");
  const [loading,setLoading]=useState(false);
  const [summary,setSummary]=useState("");
  const [insights,setInsights]=useState<any>(null);

  async function generate(){
    setLoading(true);
    setSummary(""); setInsights(null);
    try{
      const res = await api.post("/generate-insights", { csv_text: csvText, language: lang });
      setSummary(res.data.summary);
      setInsights(res.data.insights);
    }catch(e:any){
      setSummary(e?.response?.data?.message || "Error calling API");
    }finally{ setLoading(false); }
  }

  const top = useMemo(()=>{
    if(!insights?.products) return [];
    return [...insights.products].sort((a:any,b:any)=>b.confidence_score-a.confidence_score).slice(0,5);
  },[insights]);

  return (
    <div className="min-h-screen p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Merchant Intelligence Copilot</h1>
          <p className="text-slate-400 text-sm">AI‑assisted insights to support smarter business decisions.</p>
        </div>
        <select className="bg-slate-800 rounded px-3 py-2" value={lang} onChange={e=>setLang(e.target.value)}>
          <option value="en">English</option>
          <option value="hi">Hindi</option>
          <option value="mr">Marathi</option>
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-6">
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <h2 className="font-semibold mb-2">1) Paste CSV (prototype)</h2>
          <textarea
            className="w-full h-64 bg-slate-950 border border-slate-800 rounded p-3 font-mono text-xs"
            placeholder={sampleHint}
            value={csvText}
            onChange={e=>setCsvText(e.target.value)}
          />
          <button
            className="mt-3 bg-indigo-500 hover:bg-indigo-400 text-white font-semibold px-4 py-2 rounded"
            onClick={generate}
            disabled={loading}
          >
            {loading ? "Generating…" : "Generate Insights"}
          </button>
        </div>

        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <h2 className="font-semibold mb-2">2) Copilot Summary</h2>
          <div className="bg-slate-950 border border-slate-800 rounded p-3 min-h-64 whitespace-pre-wrap text-sm">
            {summary || "Your Bedrock (Nova) summary will appear here."}
          </div>
        </div>
      </div>

      <div className="mt-6 bg-slate-900 rounded-xl p-4 border border-slate-800">
        <h2 className="font-semibold mb-3">Top Products (Confidence)</h2>
        {!top.length ? (
          <p className="text-slate-400 text-sm">Run “Generate Insights” to view recommendations.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
            {top.map((p:any)=>(
              <div key={p.product_name} className="bg-slate-950 border border-slate-800 rounded-lg p-3">
                <div className="flex justify-between">
                  <div className="font-semibold">{p.product_name}</div>
                  <div className="text-xs px-2 py-1 rounded bg-slate-800">
                    {p.confidence_score}%
                  </div>
                </div>
                <div className="mt-2 text-sm text-slate-300">
                  Reorder: <b>{p.reorder?.quantity}</b> ({p.reorder?.urgency})
                </div>
                {p.anomalies?.length ? (
                  <div className="mt-2 text-xs text-amber-300">
                    Alert: {p.anomalies.map((a:any)=>a.type).join(", ")}
                  </div>
                ) : (
                  <div className="mt-2 text-xs text-slate-500">No anomalies detected.</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
