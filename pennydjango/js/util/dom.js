
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
