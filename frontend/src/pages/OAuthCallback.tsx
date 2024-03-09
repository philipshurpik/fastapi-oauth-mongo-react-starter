import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { basePath } from "../providers/env";

const OAuthCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleOAuth = async () => {
      try {
        const query = window.location.search;
        const callbackUrl = `${basePath}/api/v1/auth/google/callback${query}`;
        const response = await fetch(callbackUrl, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        navigate("/");
      } catch (error) {
        console.error("Error handling OAuth success:", error);
        navigate("/login");
      }
    };
    handleOAuth();
  }, [navigate]);

  return <div>Loading...</div>;
};

export default OAuthCallback;
