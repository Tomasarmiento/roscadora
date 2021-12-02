import "jquery/dist/jquery";       
import "bootstrap"; 
import "bootstrap/dist/css/bootstrap.min.css";
import './main.css'
import './components/monitor/monitor.component.css'

import {router} from './router/index.routes'


window.addEventListener('hashchange', () => {
    router(window.location.hash)
})