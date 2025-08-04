import {FC, ReactNode} from "react";

const Layout: FC<{ children: ReactNode }> = ({ children }) => (
    <main>
        {children}
    </main>
);

export default Layout;
