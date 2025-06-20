// Site configuration
const CONFIG = {
    // Auto-detect environment and serving directory
    get baseUrl() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            // Get the current path and remove the filename
            const path = window.location.pathname.replace(/\/[^/]*$/, '');
            return `http://${window.location.host}${path}`;
        }
        return 'https://stanleysjourney.com/basketball';
    },
    
    // Production URL (for reference)
    productionUrl: 'https://stanleysjourney.com'
};