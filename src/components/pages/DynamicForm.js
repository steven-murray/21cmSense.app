import '../../App.css';
import formJSON from '../../schema/formElement.json';
import React,{ useState, useEffect } from 'react';
import Element from '../Element';
import { FormContext } from '../../FormContext';
function DynamicForm() {
  const [elements, setElements] = useState(null);
  useEffect(() => {
    setElements(formJSON)

  }, [])
  const { fields, page_label } = elements ?? {}
  const handleSubmit = (event) => {
    event.preventDefault();

    console.log(elements)
  }
  const handleChange = (id, event) => {
    const newElements = { ...elements }
    newElements.fields.forEach(field => {
      const { field_type, key } = field;
      if (id === key) {
        switch (field_type) {
          case 'checkbox':
            field['value'] = event.target.checked;
            break;

          default:
            field['value'] = event.target.value;
            break;
        }


      }
      setElements(newElements)
    });
    console.log(elements)
  }
  return (
    <FormContext.Provider value={{ handleChange }}>
      <div className="App container">
        <h3>{page_label}</h3>
        <form>
          {fields ? fields.map((field, i) => <Element key={i} field={field} />) : null}
          <button type="submit" className="btn btn-primary" onClick={(e) => handleSubmit(e)}>Submit</button>
        </form>

      </div>
    </FormContext.Provider>
  );
}

export default DynamicForm;
