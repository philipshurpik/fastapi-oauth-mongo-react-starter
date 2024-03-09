import { render, screen } from "@testing-library/react";
import Dashboard from "./Dashboard";
import { AdminContext } from "react-admin";

test("renders dashboard", () => {
  render(
    <AdminContext>
      <Dashboard />
    </AdminContext>
  );
  const linkElement = screen.getByText(/Dashboard/i);
  expect(linkElement).toBeInTheDocument();
});
