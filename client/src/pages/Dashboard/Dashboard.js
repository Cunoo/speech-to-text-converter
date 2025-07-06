

function Dashboard() {
    const { user, isAuthenticated } = useAuth();
    
    if (!isAuthenticated) {
        return <div>Please log in to access dashboard</div>;
    }
    
    return (
        <div>
            <h1>Dashboard for {user.username}</h1>
            {/* Dashboard content */}
        </div>
    );
}

export default Dashboard;