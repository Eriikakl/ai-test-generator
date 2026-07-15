import { useState } from "react";

function App() {
  const [issueKey, setIssueKey] = useState("ABC-1");
  const [testCases, setTestCases] = useState<any[]>([]);
  const [usabilityTests, setUsabilityTests] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState<any | null>(null);

  const getTestCases = async () => {
    setLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/test-cases/${issueKey}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch test cases");
      }

      const data = await response.json();

      setTestCases(data.test_cases);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const generateUsabilityTests = async () => {
    setLoading(true);

    const response = await fetch(
      `http://localhost:8000/generate/usability-tests/${issueKey}`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    setUsabilityTests(data.usability_tests);

    setLoading(false);
  };

  return (
    <div>

      <h1>AI Test Generator</h1>

      <input
        value={issueKey}
        onChange={(e) => setIssueKey(e.target.value)}
        placeholder="Enter Jira issue key"
      />

      <button onClick={getTestCases} disabled={loading}>
        {loading ? "Loading..." : "Load Test Cases"}
      </button>
      <button onClick={generateUsabilityTests} disabled={loading}>
        {loading ? "Generating..." : "Generate Usability Tests"}
      </button>
      <div style={{ display: "flex", gap: "20px" }}>
        <div style={{ flex: 1 }}>
          <h2>Test Cases</h2>

          <ul>
            {testCases.map((tc) => (
              <li key={tc.key}>
                {tc.key} - {tc.summary}
              </li>
            ))}
          </ul>
        </div>
        <div style={{ flex: 1 }}>
          <h2>Usability Tests</h2>
          {usabilityTests.length === 0 ? (
            <p>No usability tests yet</p>
          ) : (
            <table border={1} cellPadding={8} style={{ width: "100%" }}>
              <thead>
                <tr>
                  <th>Story</th>
                  <th>Test</th>
                  <th>Priority</th>
                </tr>
              </thead>

              <tbody>
                {usabilityTests.map((ut, i) => (
                  <tr
                    key={i}
                    onClick={() => setSelected(ut)}
                    style={{ cursor: "pointer" }}
                  >
                    <td>{ut.story_key}</td>
                    <td>{ut.usability_test}</td>
                    <td>{ut.priority}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          <div style={{ flex: 1 }}>
            <h2>Details</h2>

            {selected ? (
              <div style={{ padding: 10, border: "1px solid #ccc" }}>
                <p><b>Story:</b> {selected.story_key}</p>
                <p><b>Story title:</b> {selected.story_title}</p>
                <p><b>Test:</b> {selected.usability_test}</p>
                <p><b>Priority:</b> {selected.priority}</p>
              </div>
            ) : (
              <p>Select a usability test</p>
            )}
          </div>
        </div>

      </div>

    </div>
  );
}

export default App;