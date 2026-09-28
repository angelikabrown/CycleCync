import { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import DailyCheckInForm from "./components/DailyCheckInForm";
import CheckInHistory from "./components/CheckInHistory";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!sessionStorage.getItem("token")
  );

  const [refreshTrigger, setRefreshTrigger] = useState(0);

  if (!isLoggedIn) {
    return <Login onLogin={() => setIsLoggedIn(true)} />;
  }

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
