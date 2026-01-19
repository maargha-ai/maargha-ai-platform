import { useNavigate } from "react-router-dom";
import "../styles/button.css";
const Button = () => {
  const navigate = useNavigate();
  return (
    <button
      className="button"
      onClick={() => navigate("/register")}
    >
      GetStarted →
    </button>
  );
};
export default Button;


