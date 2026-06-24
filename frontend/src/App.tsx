import { useState } from "react";

function App() {
  const [issueKey, setIssueKey] = useState("ABC-1");
  const [testCases, setTestCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const generateTests = async () => {
    setLoading(true);

    const response = await fetch(
      `http://localhost:8000/generate/test-cases/${issueKey}`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    setTestCases(data.test_cases);

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

      <button onClick={generateTests} disabled={loading}>
        {loading ? "Generating..." : "Generate Test Cases"}
      </button>
      
      <h2>Test Cases</h2>

      <ul>
        {testCases.map((tc, i) => (
          <li key={i}>{tc.test_case}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;