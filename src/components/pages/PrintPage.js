import '../../App.css';
import React from 'react';


class PrintPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      localStoragePairs: []
    };
   
  }

  componentDidMount() {
    this.getExistingArray();
  }

  getExistingArray() {

    for (var i = 0; i < localStorage.length; i++) {

      var key = localStorage.key(i);
      var value = localStorage.getItem(key);

      var updatedLocalStoragePairs = this.state.localStoragePairs;
      updatedLocalStoragePairs.push({ 'keyName': key, 'valueName': value });

      this.setState({ localStoragePairs: updatedLocalStoragePairs });
    }
    console.log("complete localStoragePairs:", this.state.localStoragePairs);

    if (localStorage.getItem('inputs')) {
      var storedInputs = localStorage.getItem('inputs');
      this.setState({ inputs: storedInputs }, function () { console.log("from localStorage We got:", this.state.inputs); });
    }
  }

  
  

  render() {
    var LocalSotrageContent = this.state.localStoragePairs.map((value, index) => {
      return <tr key={index}> <td>{value.keyName}</td>  <td>{value.valueName}</td> </tr>
    });


    return (
      <div>
        <table>
          <thead>
            <tr>
              <th>All Local Storage objects by Name</th>
              <th>All Local Storage objects by Value</th>
            </tr>
          </thead>
          <tbody>
            {LocalSotrageContent}
          </tbody>
        </table>
        <br />
      </div>
    );
  }
}

export default PrintPage;
