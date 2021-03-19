import React, {Component} from 'react';
import {v4 as uuidv4} from 'uuid'

class TableRow extends Component {
  render() {
    return (
        <tr key={uuidv4()}>
          <th scope="row">{this.props.row["employeeId"]}</th>
          <td>{this.props.row["payPeriod"]["startDate"]}</td>
          <td>{this.props.row["payPeriod"]["endDate"]}</td>
          <td>{this.props.row["amountPaid"]}</td>
        </tr>
    );
  }
}

export default TableRow;
