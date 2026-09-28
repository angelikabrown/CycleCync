import { useState } from "react";
import DailyCheckInForm from "./components/DailyCheckInForm";
import CheckInHistory from "./components/CheckInHistory";
import Dashboard from "./components/Dashboard";

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  return (
    <div>
      <h1>Hello CycleCync</h1>

      <Dashboard />

      <DailyCheckInForm
        onCheckInSaved={() =>
          setRefreshTrigger((current) => current + 1)
        }
      />

      <CheckInHistory refreshTrigger={refreshTrigger} />
    </div>
  );
}

export default App;
