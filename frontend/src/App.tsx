import { useState } from "react";
import "./App.css";

type VerificationResult = {
  [key: string]: any;
};

function App() {
  const [disruption, setDisruption] = useState(
    "Severe flooding has disrupted a component supplier in Chennai. Production and transportation may be affected."
  );

  const [result, setResult] = useState<VerificationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const scrollToSection = (id: string) => {
    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  const verifyDisruption = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "/api/verify",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            disruption: disruption,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Verification failed");
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      setError(
        "Unable to connect to VeriChain AI. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* ================= HEADER ================= */}

      <header className="header">
        <div className="brand">
          <div className="logo">V</div>

          <div>
            <h1>VeriChain AI</h1>
            <p>Multi-Agent Supply Chain Verification Engine</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Online
        </div>
      </header>


      {/* ================= HERO ================= */}

      <section className="hero">

        <div className="hero-text">

          <div className="badge">
            ✦ AI-POWERED VERIFICATION
          </div>

          <h2>
            Trusted Supply Chains
            <span> with AI</span>
          </h2>

          <p>
            Verify supply chain disruptions using intelligent
            multi-agent analysis, evidence verification,
            contradiction detection, and risk assessment.
          </p>

          <div className="hero-points">
            <div>✓ Multi-Agent Verification</div>
            <div>✓ Evidence-Based Decisions</div>
            <div>✓ Real-Time Risk Assessment</div>
          </div>

        </div>


        <div className="hero-info">

          <div className="info-card">
            <span>🌐</span>

            <div>
              <strong>Global Supply Chain</strong>
              <p>Connected verification intelligence</p>
            </div>
          </div>


          <div className="info-card">
            <span>🛡️</span>

            <div>
              <strong>Trust & Transparency</strong>
              <p>Evidence-backed verification</p>
            </div>
          </div>

        </div>

      </section>


      {/* ================= VERIFICATION ================= */}

      <main className="container">

        <section className="verification-card">

          <div className="section-label">
            SUPPLY CHAIN ANALYSIS
          </div>

          <h2>Describe the disruption</h2>

          <p className="section-description">
            Enter a supply chain event and let VeriChain AI
            verify the impact through multiple intelligent agents.
          </p>

          <textarea
            value={disruption}
            onChange={(e) => setDisruption(e.target.value)}
            placeholder="Describe the supply chain disruption..."
          />

          <button
            className="verify-button"
            onClick={verifyDisruption}
            disabled={loading || !disruption.trim()}
          >

            {loading ? (
              <>
                <span className="spinner"></span>
                Verifying...
              </>
            ) : (
              <>
                Verify Disruption
                <span>→</span>
              </>
            )}

          </button>

        </section>


        {/* ================= ERROR ================= */}

        {error && (
          <div className="error-box">
            ⚠️ {error}
          </div>
        )}


        {/* ================= FEATURES ================= */}

        <section className="features">

          <button
            type="button"
            className="feature-card"
            onClick={() => scrollToSection("risk-analysis")}
          >
            <div className="feature-icon pink">◈</div>

            <h3>Risk Assessment</h3>

            <p>
              Calculate disruption risk and identify
              affected supply chain areas.
            </p>
          </button>


          <button
            type="button"
            className="feature-card"
            onClick={() => scrollToSection("agent-pipeline")}
          >
            <div className="feature-icon purple">◎</div>

            <h3>Multi-Agent Verification</h3>

            <p>
              Multiple verification agents analyze
              the event independently.
            </p>
          </button>


          <button
            type="button"
            className="feature-card"
            onClick={() => scrollToSection("contradiction")}
          >
            <div className="feature-icon rose">✦</div>

            <h3>Contradiction Detection</h3>

            <p>
              Detect conflicting claims and resolve
              them using independent evidence.
            </p>
          </button>


          <button
            type="button"
            className="feature-card"
            onClick={() => scrollToSection("action-plan")}
          >
            <div className="feature-icon lavender">✓</div>

            <h3>Actionable Insights</h3>

            <p>
              Generate verified decisions and
              recommended next actions.
            </p>
          </button>

        </section>


        {/* ================= RESULTS ================= */}

        {result && (

          <section className="results">

            <div className="results-heading">

              <div>

                <div className="section-label">
                  VERIFICATION COMPLETE
                </div>

                <h2>Analysis Results</h2>

              </div>

              <div className="verified-badge">
                ✓ Verified
              </div>

            </div>


            {/* ================= RISK + LOCATION ================= */}

            <div className="result-grid">

              <div className="result-card">

                <h3>Risk Score</h3>

                <div className="risk-score">
                  {result.risk?.risk_score ?? "N/A"}
                </div>

                <div
                  className={`risk-level ${
                    result.risk?.risk_level?.toLowerCase() || ""
                  }`}
                >
                  {result.risk?.risk_level ?? "UNKNOWN"}
                </div>

              </div>


              <div className="result-card">

                <h3>Supply Chain Impact</h3>

                <div className="impact-value">
                  {result.supply_chain?.impact_area ??
                    "Not available"}
                </div>

                <p>
                  <strong>Location:</strong>{" "}
                  {result.supply_chain?.affected_location ??
                    "Unknown"}
                </p>

                <p>
                  <strong>Supplier:</strong>{" "}
                  {result.supply_chain?.affected_supplier ??
                    "Unknown"}
                </p>

              </div>

            </div>


            {/* ================= RISK ANALYSIS ================= */}

            {result.risk?.reasons && (

              <div
                className="result-card full"
                id="risk-analysis"
              >

                <h3>Risk Analysis</h3>

                <div className="reason-list">

                  {result.risk.reasons.map(
                    (reason: string, index: number) => (

                      <div
                        className="reason"
                        key={index}
                      >
                        <span>✓</span>
                        {reason}
                      </div>

                    )
                  )}

                </div>

              </div>

            )}


            {/* ================= AGENT PIPELINE ================= */}

            <div
              className="result-card full"
              id="agent-pipeline"
            >

              <h3>Agent Verification Pipeline</h3>

              <div className="pipeline">

                {[
                  "Supply Chain Mapping",
                  "Risk Calculation",
                  "Action Planning",
                  "Calculation Verification",
                  "Evidence Verification",
                  "Contradiction Detection",
                  "Independent Evidence",
                  "Contradiction Resolution",
                ].map((agent, index) => (

                  <div
                    className="agent"
                    key={index}
                  >

                    <span className="agent-check">
                      ✓
                    </span>

                    <span>{agent}</span>

                  </div>

                ))}

              </div>

            </div>


            {/* ================= CONTRADICTION ================= */}

            {result.contradiction_result && (

              <div
                className="result-card full"
                id="contradiction"
              >

                <h3>
                  Contradiction Detection
                </h3>


                <div className="action-priority">

                  <strong>Status:</strong>{" "}

                  {result.contradiction_result.result
                    ?.contradiction_detected
                    ? "Contradiction Detected"
                    : "No Contradiction"}

                </div>


                {result.contradiction_result.result
                  ?.contradictions?.map(
                    (item: any, index: number) => (

                      <div
                        className="action-section"
                        key={index}
                      >

                        <h4>
                          Conflict {index + 1}
                        </h4>

                        <p>
                          <strong>Claim 1:</strong>{" "}
                          {item.claim1}
                        </p>

                        <p>
                          <strong>Claim 2:</strong>{" "}
                          {item.claim2}
                        </p>

                        <p>
                          <strong>Description:</strong>{" "}
                          {item.description}
                        </p>

                      </div>

                    )
                  )}

              </div>

            )}


            {/* ================= INDEPENDENT EVIDENCE ================= */}

            {result.resolution_result && (

              <div className="result-card full">

                <h3>
                  Independent Evidence & Resolution
                </h3>

                <div className="action-priority">

                  <strong>Status:</strong>{" "}

                  {result.resolution_result.status ??
                    "N/A"}

                </div>

                <p>
                  {result.resolution_result.reason ??
                    "No resolution information available."}
                </p>

                {result.resolution_result.accepted_claim && (

                  <p>
                    <strong>Accepted Claim:</strong>{" "}
                    {result.resolution_result.accepted_claim}
                  </p>

                )}

              </div>

            )}


            {/* ================= AI ACTION PLAN ================= */}

            {result.action_plan && (

              <div
                className="result-card full action-plan-card"
                id="action-plan"
              >

                <div className="section-label">
                  AI ACTION PLAN
                </div>

                <h3>
                  Recommended Response
                </h3>


                <div className="action-priority">

                  <strong>Priority:</strong>{" "}

                  {result.action_plan.revised_priority ??
                    result.action_plan.priority ??
                    "N/A"}

                </div>


                <div className="action-section">

                  <h4>Immediate Actions</h4>

                  <ul>

                    {(
                      result.action_plan.revised_immediate_actions ??
                      result.action_plan.immediate_actions ??
                      []
                    ).map(
                      (action: string, index: number) => (

                        <li key={index}>
                          {action}
                        </li>

                      )
                    )}

                  </ul>

                </div>


                <div className="action-section">

                  <h4>Short-Term Actions</h4>

                  <ul>

                    {(
                      result.action_plan.revised_short_term_actions ??
                      result.action_plan.short_term_actions ??
                      []
                    ).map(
                      (action: string, index: number) => (

                        <li key={index}>
                          {action}
                        </li>

                      )
                    )}

                  </ul>

                </div>


                <div className="action-section">

                  <h4>Recommendation</h4>

                  <p>
                    {result.action_plan.revised_recommendation ??
                      result.action_plan.recommendation ??
                      "No recommendation available."}
                  </p>

                </div>


                <div className="action-section">

                  <h4>Evidence Required</h4>

                  <ul>

                    {(
                      result.action_plan.evidence_to_collect ??
                      result.action_plan.required_evidence ??
                      []
                    ).map(
                      (evidence: string, index: number) => (

                        <li key={index}>
                          {evidence}
                        </li>

                      )
                    )}

                  </ul>

                </div>


                <div className="action-section">

                  <h4>Remaining Uncertainties</h4>

                  <ul>

                    {(
                      result.action_plan.remaining_uncertainties ??
                      result.action_plan.uncertainties ??
                      []
                    ).map(
                      (uncertainty: string, index: number) => (

                        <li key={index}>
                          {uncertainty}
                        </li>

                      )
                    )}

                  </ul>

                </div>

              </div>

            )}


            {/* ================= FINAL DECISION ================= */}

            {result.decision && (

              <div className="decision-card">

                <div className="section-label">
                  FINAL DECISION
                </div>

                <div className="decision">
                  {result.decision.decision ??
                    "N/A"}
                </div>

                <p>
                  {result.decision.reason ??
                    "No decision reason available."}
                </p>

              </div>

            )}


            {/* ================= RAW DATA ================= */}

            <details className="raw-result">

              <summary>
                View Verification Data
              </summary>

              <pre>
                {JSON.stringify(
                  result,
                  null,
                  2
                )}
              </pre>

            </details>

          </section>

        )}

      </main>


      {/* ================= FOOTER ================= */}

      <footer>

        <strong>VeriChain AI</strong>

        <span>•</span>

        Multi-Agent Supply Chain Verification Engine

      </footer>

    </div>
  );
}

export default App;