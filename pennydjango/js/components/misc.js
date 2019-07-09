import React from 'react'

export const Switch = ({label, checked, onClick}) =>
    <div onClick={e => e.stopPropagation()} style={{display: 'flex'}}>
        <label class="switch">
            <input type="checkbox" checked={checked} />
            <span class="slider round" onClick={e => onClick(e)}></span>
        </label>
        <div style={{margin: 'auto', paddingLeft: 8}} onClick={e => onClick(e)}>{label}</div>
    </div>

export const SettingsGear = ({onClick}) =>
    <div className="settings-gear" onClick={(e) => onClick(e)}>
        <i className="material-icons">settings</i>
    </div>
