import { create } from "zustand";

type State = {
  role: "Operator" | "Manufacturing Engineer" | "Operations Manager";
  setRole: (role: State["role"]) => void;
};

export const useCommandCenterStore = create<State>((set) => ({
  role: "Operator",
  setRole: (role) => set({ role })
}));
