import React, { useContext } from 'react'
import { FormContext } from '../../FormContext';

const Input = ({ id, label, placeholder, value }) => {
    const { handleChange } = useContext(FormContext)
    return (
        <div className="mb-3">
            <label htmlFor="id" className="form-label">{label}</label>
            <input type="text" className="form-control" id="id" aria-describedby="emailHelp"
                placeholder={placeholder ? placeholder : ''}
                value={value}
                onChange={event => handleChange(id, event)}
            />
        </div>
    )
}

export default Input
