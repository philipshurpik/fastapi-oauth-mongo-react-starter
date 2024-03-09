import { FormEvent, ReactElement } from "react";
import { basePath } from "../providers/env";

import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardActions from "@mui/material/CardActions";
import TextField from "@mui/material/TextField";
import { Notification } from "react-admin";
import authStyles from "./authStyles";
import LockIcon from "@mui/icons-material/Lock";

interface AuthProps {
  submit(event: FormEvent): void;
  setEmail(value: string): void;
  setPassword?(value: string): void;
  actionName: string;
  extraActions?: ReactElement;
}

const Auth: React.FC<AuthProps> = ({
  submit,
  setEmail,
  setPassword,
  actionName,
  extraActions,
}) => {
  const handleGoogleAuth = async () => {
    try {
      const response = await fetch(`${basePath}/api/v1/auth/google/authorize`);
      const data = await response.json();
      // Redirect to the Google Auth URL
      window.location.href = data.authorization_url;
    } catch (error) {
      console.error("Failed to fetch Google auth URL", error);
    }
  };

  return (
    <form noValidate onSubmit={submit}>
      <div style={authStyles.main}>
        <Card sx={authStyles.card}>
          <div style={authStyles.avatar}>
            <Avatar>
              <LockIcon />
            </Avatar>
          </div>
          <CardHeader
            title={`Auth - ${actionName}`}
            sx={authStyles.header}
          />
          <div style={authStyles.form}>
            <div>
              <TextField
                id="email"
                label="Email"
                type="email"
                onChange={(e) => setEmail(e.target.value)}
                fullWidth
              />
            </div>

            {setPassword && (
              <div>
                <TextField
                  id="password"
                  label="Password"
                  type="password"
                  fullWidth
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            )}
          </div>
          <CardActions sx={authStyles.actions}>
            <Button variant="contained" type="submit" color="primary" fullWidth>
              {actionName}
            </Button>
          </CardActions>
          <Divider />
          <CardActions>
            <Button
              variant="contained"
              color="secondary"
              fullWidth
              onClick={handleGoogleAuth}
            >
              Continue with Google
            </Button>
          </CardActions>
          <Divider />
          <CardActions sx={authStyles.actions}>
            Don't have account? {extraActions}
          </CardActions>
        </Card>
        <Notification />
      </div>
    </form>
  );
};

export default Auth;
