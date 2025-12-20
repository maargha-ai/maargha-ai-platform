import "../styles/register.css";

export default function Register() {
  return (
    <div className="register-wrapper">
      {/* STAR BACKGROUND */}
      <div className="stars-layer">
        {[...Array(120)].map((_, i) => (
          <span key={i} className="star" />
        ))}
      </div>

      {/* FORM CARD */}
      <div className="register-card">
        <h2>Create Account</h2>

        <form>
          <input type="text" placeholder="Full Name" />
          <input type="email" placeholder="Email" />
          <input type="password" placeholder="Password" />

          <button type="submit">Register</button>
        </form>
      </div>
    </div>
  );
}
