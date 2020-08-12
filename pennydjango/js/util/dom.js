import React from 'react'

export const tooltip = (text, placement='bottom') => ({
    'data-original-title': text,
    onMouseEnter: (e) => {
        $('[data-toggle="tooltip"]').tooltip('hide')
        $(e.target).tooltip()
    },
    onMouseLeave: (e) => {
        $('[data-toggle="tooltip"]').tooltip('hide')
        $(e.target).tooltip('hide')
    },
    'data-toggle': 'tooltip',
    'data-placement': placement,
})

export class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }
  
    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true };
    }
  
    componentDidCatch(error, errorInfo) {
        // You can also log the error to an error reporting service
        console.error(error, errorInfo);
    }
  
    render() {
        if (this.state.hasError) {
          // You can render any custom fallback UI
          return <small style={{color: 'red'}}><br/><br/>Something went wrong while loading this component...</small>;
        }
  
        return this.props.children; 
    }
}

export const pushFilterState = (data) => {
    const qs_params_string = $.param(data)
    const push_url = `${window.location.origin}${window.location.pathname}?${qs_params_string}`
    console.log(data, push_url, qs_params_string)
    history.pushState(qs_params_string, "", push_url)
}
