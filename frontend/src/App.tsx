import CheckInHistory from "./components/CheckInHistory";
import Login from "./components/Login";
import DailyCheckInForm from "./components/DailyCheckInForm";

function App() {
  return (
    <div>
      <h1>Hello CycleCync</h1>
      <Login />

      <DailyCheckInForm />

      <CheckInHistory />



    </div>
  );
}


export default App;
