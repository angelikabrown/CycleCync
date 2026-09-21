import { useState } from "react";
import CheckInHistory from "./components/CheckInHistory";
import DailyCheckInForm from "./components/DailyCheckInForm";

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  return (
    <div>
      <h1>Hello CycleCync</h1>

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
