import React, { useContext } from 'react'
import { FormContext } from '../../FormContext';
const Select = ({ id, label, placeholder, value, options }) => {
    const { handleChange } = useContext(FormContext)

    return (
        <>
            <label className="form-label">{label}</label>
            <select className="form-select" aria-label="Default select example"
                onChange={event => handleChange(id, event)}
            >
                <option >Select Value</option>
                {options.length > 0 && options.map((option, i) =>
                    <option value={option.option_label} key={i}>{option.option_label}</option>

                )}
            </select>
        </>
    )
}

export default Select
