import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";

type JiraStory = {
  key: string;
  summary: string;
};

type TestCase = {
  key: string;
  summary: string;
};

type UsabilityTest = {
  id: string;
  story_key: string;
  story_title: string;
  title: string;
  description: string;
  test_case_keys: string[];
  priority: string;
  status: "pending" | "approved" | "rejected";
};

function App() {
  const [search, setSearch] = useState("");
  const [stories, setStories] = useState<JiraStory[]>([]);
  const [selectedStory, setSelectedStory] = useState<JiraStory | null>(null);

  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [usabilityTests, setUsabilityTests] = useState<UsabilityTest[]>([]);
  const [selectedTest, setSelectedTest] = useState<UsabilityTest | null>(null);

  const [loading, setLoading] = useState(false);
  const [searching, setSearching] = useState(false);
  const [apiConnected, setApiConnected] = useState(false);
  const [error, setError] = useState("");


  // API health check
  useEffect(() => {
    const checkApi = async () => {
      try {
        const response = await fetch(`${API_URL}/health`);
        setApiConnected(response.ok);
      } catch {
        setApiConnected(false);
      }
    };

    checkApi();
  }, []);

  // Jira story search
  const searchStories = async () => {
    if (!search.trim()) {
      setStories([]);
      return;
    }

    setSearching(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/jira/stories/search?q=${encodeURIComponent(
          search.trim()
        )}`
      );

      const data = await response.json();

      console.log("JIRA SEARCH RESPONSE:", data);

      if (!response.ok) {
        throw new Error(
          data.message || "Failed to search Jira stories"
        );
      }

      setStories(data.stories || []);
    } catch (error) {
      setStories([]);

      setError(
        error instanceof Error
          ? error.message
          : "Failed to search Jira stories"
      );
    } finally {
      setSearching(false);
    }
  };

  // Select Jira story
  const selectStory = (story: JiraStory) => {
    setSelectedStory(story);
    setSearch("");
    setStories([]);
    setTestCases([]);
    setUsabilityTests([]);
    setSelectedTest(null);
    setError("");
  };


  // Load test cases from selected Jira story
  const loadTestCases = async () => {
    if (!selectedStory) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/test-cases/${selectedStory.key}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Failed to load test cases"
        );
      }

      setTestCases(data.test_cases || []);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to load test cases"
      );
    } finally {
      setLoading(false);
    }
  };

  // Generate usability tests from selected Jira story
  const generateUsabilityTests = async () => {
    if (!selectedStory) return;

    setLoading(true);
    setError("");
    setSelectedTest(null);

    try {
      const response = await fetch(
        `${API_URL}/generate/usability-tests/${selectedStory.key}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Failed to generate usability tests"
        );
      }

      const tests: UsabilityTest[] = (
        data.usability_tests || []
      ).map(
        (
          test: Omit<UsabilityTest, "status" | "id">,
          index: number
        ) => ({
          ...test,
          id: `UT-${index + 1}`,
          story_key: test.story_key || selectedStory.key,
          story_title:
            test.story_title || selectedStory.summary,
          test_case_keys: test.test_case_keys || [],
          status: "pending",
        })
      );

      setUsabilityTests(tests);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to generate usability tests"
      );
    } finally {
      setLoading(false);
    }
  };

  // Update usability test approval status (approve/reject)
  const updateTestStatus = (
    id: string,
    status: "approved" | "rejected"
  ) => {
    setUsabilityTests((tests) =>
      tests.map((test) =>
        test.id === id
          ? {
            ...test,
            status,
          }
          : test
      )
    );

    if (selectedTest?.id === id) {
      setSelectedTest((test) =>
        test
          ? {
            ...test,
            status,
          }
          : null
      );
    }
  };


  // Edit selected test
  const updateSelectedTest = (
    field: keyof UsabilityTest,
    value: string
  ) => {
    if (!selectedTest) return;

    const updatedTest = {
      ...selectedTest,
      [field]: value,
    };

    setSelectedTest(updatedTest);

    setUsabilityTests((tests) =>
      tests.map((test) =>
        test.id === updatedTest.id ? updatedTest : test
      )
    );
  };


  // Push approved tests to Jira
  const pushApprovedTests = async () => {
    if (!selectedStory) return;

    const approvedTests = usabilityTests
      .filter((test) => test.status === "approved")
      .map((test) => ({
        story_key: test.story_key,
        story_title: test.story_title,
        title: test.title,
        description: test.description,
        test_case_keys: test.test_case_keys,
        priority: test.priority,
      }));

    if (approvedTests.length === 0) {
      setError("No approved usability tests to push.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/push/usability-tests/${selectedStory.key}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            usability_tests: approvedTests,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Failed to push usability tests"
        );
      }

      setUsabilityTests((tests) =>
        tests.filter((test) => test.status !== "approved")
      );

      setSelectedTest(null);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to push usability tests"
      );
    } finally {
      setLoading(false);
    }
  };


  // Calculate the number of approved, rejected and pending usability tests
  const approvedCount = useMemo(
    () =>
      usabilityTests.filter(
        (test) => test.status === "approved"
      ).length,
    [usabilityTests]
  );

  const rejectedCount = useMemo(
    () =>
      usabilityTests.filter(
        (test) => test.status === "rejected"
      ).length,
    [usabilityTests]
  );

  const pendingCount = useMemo(
    () =>
      usabilityTests.filter(
        (test) => test.status === "pending"
      ).length,
    [usabilityTests]
  );


  return (
    <div className="app">
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <div className="brand-mark">✦</div>

            <div>
              <span className="eyebrow">
                AI TEST GENERATOR
              </span>

              <h1>Test Intelligence</h1>
            </div>
          </div>

          <div
            className={`connection ${apiConnected
              ? "connected"
              : "disconnected"
              }`}
          >
            <span className="connection-dot" />

            {apiConnected
              ? "API connected"
              : "API offline"}
          </div>
        </div>
      </header>

      <main className="container">
        {/* Introduction and workflow overview */}

        <section className="hero">
          <div>
            <span className="section-label">
              AI-ASSISTED TESTING
            </span>

            <h2>
              Turn Jira stories into
              <span> better usability tests.</span>
            </h2>

            <p>
              Combine AI intelligence with human judgment
              to generate, review and approve usability
              tests before they are pushed to Jira.
            </p>
          </div>
        </section>

        {/* story selector */}

        <section className="story-section">
          <div className="section-heading">
            <div>
              <span className="section-label">
                SOURCE
              </span>

              <h3>Select Jira Story</h3>
            </div>

            {selectedStory && (
              <span className="selected-story">
                {selectedStory.key}
              </span>
            )}
          </div>

          <div className="search-wrapper">
            <span className="search-icon">⌕</span>

            <input
              type="text"
              value={search}
              onChange={(event) => {
                setSelectedStory(null);
                setSearch(event.target.value);
                setStories([]);
                setError("");
              }}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  searchStories();
                }
              }}
              placeholder="Search Jira stories..."
            />

            <button
              type="button"
              className="search-button"
              onClick={searchStories}
              disabled={
                searching || !search.trim()
              }
            >
              {searching
                ? "Searching..."
                : "Search"}
            </button>
          </div>

          {stories.length > 0 && (
            <div className="story-results">
              {stories.map((story) => (
                <button
                  type="button"
                  className="story-result"
                  key={story.key}
                  onClick={() =>
                    selectStory(story)
                  }
                >
                  <span className="story-key">
                    {story.key}
                  </span>

                  <span className="story-summary">
                    {story.summary}
                  </span>

                  <span className="result-arrow">
                    →
                  </span>
                </button>
              ))}
            </div>
          )}

          {selectedStory && (
            <div className="selected-story-card">
              <div className="story-icon">J</div>

              <div className="selected-story-info">
                <span>
                  {selectedStory.key}
                </span>

                <strong>
                  {selectedStory.summary}
                </strong>
              </div>

              <button
                type="button"
                className="change-story"
                onClick={() => {
                  setSelectedStory(null);
                  setSearch("");
                  setStories([]);
                  setTestCases([]);
                  setUsabilityTests([]);
                  setSelectedTest(null);
                  setError("");
                }}
              >
                Change
              </button>
            </div>
          )}

          {selectedStory && (
            <div className="story-actions">
              <button
                type="button"
                className="button secondary"
                onClick={loadTestCases}
                disabled={loading}
              >
                Load test cases
              </button>

              <button
                type="button"
                className="button primary"
                onClick={generateUsabilityTests}
                disabled={loading}
              >
                {loading
                  ? "Generating..."
                  : "✦ Generate usability tests"}
              </button>
            </div>
          )}
        </section>

        {error && (
          <div className="error">
            <span>!</span>
            {error}
          </div>
        )}

        {/* review summary */}

        {usabilityTests.length > 0 && (
          <section className="review-bar">
            <div className="review-title">
              <span className="section-label">
                REVIEW STATUS
              </span>

              <strong>
                {pendingCount > 0
                  ? `${pendingCount} test${pendingCount !== 1
                    ? "s"
                    : ""
                  } waiting for review`
                  : "All tests reviewed"}
              </strong>
            </div>

            <div className="review-stats">
              <div>
                <strong>
                  {usabilityTests.length}
                </strong>

                <span>Total</span>
              </div>

              <div className="stat-approved">
                <strong>
                  {approvedCount}
                </strong>

                <span>Approved</span>
              </div>

              <div className="stat-rejected">
                <strong>
                  {rejectedCount}
                </strong>

                <span>Rejected</span>
              </div>
            </div>
          </section>
        )}

        <section className="workspace">
          {/* test cases */}

          <div className="panel">
            <div className="panel-header">
              <div>
                <span className="panel-label">
                  JIRA
                </span>

                <h3>Test Cases</h3>
              </div>

              <span className="count">
                {testCases.length}
              </span>
            </div>

            {testCases.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">
                  ✓
                </div>

                <strong>
                  No test cases loaded
                </strong>

                <p>
                  Load the test cases linked to the
                  selected Jira story.
                </p>
              </div>
            ) : (
              <div className="test-case-list">
                {testCases.map((testCase) => (
                  <div
                    className="test-case"
                    key={testCase.key}
                  >
                    <span className="test-case-key">
                      {testCase.key}
                    </span>

                    <span>
                      {testCase.summary}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* usability tests */}

          <div className="panel">
            <div className="panel-header">
              <div>
                <span className="panel-label">
                  AI GENERATED
                </span>

                <h3>Usability Tests</h3>
              </div>

              <span className="count">
                {usabilityTests.length}
              </span>
            </div>

            {usabilityTests.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon sparkle">
                  ✦
                </div>

                <strong>
                  No usability tests yet
                </strong>

                <p>
                  Generate usability tests from the
                  selected Jira story.
                </p>
              </div>
            ) : (
              <div className="usability-list">
                {usabilityTests.map((test) => (
                  <button
                    type="button"
                    key={test.id}
                    className={`usability-test ${selectedTest?.id ===
                      test.id
                      ? "selected"
                      : ""
                      }`}
                    onClick={() =>
                      setSelectedTest(test)
                    }
                  >
                    <div className="usability-content">
                      <div className="usability-id">
                        {test.id}
                      </div>

                      <strong>
                        {test.title}
                      </strong>
                    </div>

                    <span
                      className={`status-badge ${test.status}`}
                    >
                      {test.status}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* review usability tests */}

          <div className="panel review-panel">
            <div className="panel-header">
              <div>
                <span className="panel-label">
                  REVIEW
                </span>

                <h3>Details</h3>
              </div>
            </div>

            {!selectedTest ? (
              <div className="empty-state review-empty">
                <div className="review-arrow">
                  ↗
                </div>

                <strong>
                  Select a test
                </strong>

                <p>
                  Select an AI-generated usability test
                  to review, edit or approve it.
                </p>
              </div>
            ) : (
              <div className="details">
                <div className="detail">
                  <span>Story</span>

                  <strong>
                    {selectedTest.story_key}
                  </strong>
                </div>

                <div className="detail">
                  <span>Priority</span>

                  <select
                    value={
                      selectedTest.priority
                    }
                    onChange={(event) =>
                      updateSelectedTest(
                        "priority",
                        event.target.value
                      )
                    }
                  >
                    <option value="High">
                      High
                    </option>

                    <option value="Medium">
                      Medium
                    </option>

                    <option value="Low">
                      Low
                    </option>
                  </select>
                </div>

                <div className="detail test-editor">
                  <span>
                    Usability test title
                  </span>

                  <input
                    className="test-editor-input"
                    value={selectedTest.title}
                    onChange={(event) =>
                      updateSelectedTest(
                        "title",
                        event.target.value
                      )
                    }
                  />

                  <span>
                    Usability test description
                  </span>

                  <textarea
                    className="test-editor-input"
                    value={selectedTest.description}
                    onChange={(event) =>
                      updateSelectedTest(
                        "description",
                        event.target.value
                      )
                    }
                  />
                </div>

                <div className="current-status">
                  <span>
                    Current status
                  </span>

                  <span
                    className={`status-badge ${selectedTest.status}`}
                  >
                    {selectedTest.status}
                  </span>
                </div>

                <div className="review-actions">
                  <button
                    type="button"
                    className="button reject"
                    onClick={() =>
                      updateTestStatus(
                        selectedTest.id,
                        "rejected"
                      )
                    }
                  >
                    Reject
                  </button>

                  <button
                    type="button"
                    className="button approve"
                    onClick={() =>
                      updateTestStatus(
                        selectedTest.id,
                        "approved"
                      )
                    }
                  >
                    ✓ Approve
                  </button>
                </div>
              </div>
            )}
          </div>
        </section>

        {/* push to jira */}

        <section className="push-card">
          <div className="push-content">
            <div className="push-icon">↑</div>

            <div>
              <span className="section-label">
                READY FOR JIRA
              </span>

              <h3>
                {approvedCount} approved test
                {approvedCount !== 1
                  ? "s"
                  : ""}
              </h3>

              <p>
                Only approved and reviewed usability
                tests will be pushed to Jira.
              </p>
            </div>
          </div>

          <button
            type="button"
            className="button primary push-button"
            onClick={pushApprovedTests}
            disabled={
              loading || approvedCount === 0
            }
          >
            Push approved to Jira
            <span>→</span>
          </button>
        </section>
      </main>
    </div>
  );
}

export default App;