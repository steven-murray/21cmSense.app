import React from 'react'
import Checkbox from './elements/Checkbox';
import Input from './elements/Input';
import Select from './elements/Select';
const Element = ({ field: { type, id, label, placeholder, value, options } }) => {

    switch (type) {
        case 'text':
            return (<Input
                id={id}
                label={label}
                placeholder={placeholder}
                value={value}

            />)
        case 'select':
            return (<Select
                id={id}
                label={label}
                placeholder={placeholder}
                value={value}
                options={options}
            />)
        case 'checkbox':
            return (<Checkbox
                id={id}
                label={label}
                value={value}
            />)

        default:
            return null;
    }


}

export default Element
