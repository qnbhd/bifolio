# Database choice

The need for databases is determined by the need to store user data and transactions, as well as user sessions and
filling out the black list for JWT tokens.

## Few words about data

### User data:

- Data has a clear structure, changes will not happen often
- Support for unstructured data is not required

### Session data

Storage of tokens with a retention period

## Comparison

### Session storage

Let's compare MemCached and Redis.

<table>
    <tbody>
     <tr>
          <th>&nbsp;</th>
          <th style="text-align: center;">Memcached<br> </th>
          <th style="text-align: center;">Redis</th>
     </tr>
     <tr>
          <td>Sub-millisecond latency</td>
          <td style="text-align: center;">Yes</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Developer ease of use<br> </td>
          <td style="text-align: center;">Yes</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Data partitioning</td>
          <td style="text-align: center;">Yes</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Support for a broad set of programming languages</td>
          <td style="text-align: center;">Yes</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Advanced data structures</td>
          <td style="text-align: center;">-</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Multithreaded architecture</td>
          <td style="text-align: center;">Yes</td>
          <td style="text-align: center;">-</td>
     </tr>
     <tr>
          <td>Snapshots</td>
          <td style="text-align: center;">-</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Replication</td>
          <td style="text-align: center;">-</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Transactions<br> </td>
          <td style="text-align: center;">-</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Pub/Sub</td>
          <td style="text-align: center;">-</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Lua scripting</td>
          <td style="text-align: center;">-</td>
          <td style="text-align: center;">Yes</td>
     </tr>
     <tr>
          <td>Geospatial support</td>
          <td style="text-align: center;">-</td>
          <td style="text-align: center;">Yes</td>
     </tr>
    </tbody>
</table>

Based on the large number of users, Redis was chosen for this project.

## Users and transactions

Since the data has a clear structure, we do not need a NoSQL database, we will choose a relational DBMS.

<table>
<thead>
<tr>
<th style="text-align:center">OLTP</th>
<th style="text-align:center">OLAP</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">Large and small datasets</td>
<td style="text-align:center">Large datasets focused on reporting/analysis</td>
</tr>
<tr>
<td style="text-align:center">Transactional data (the raw, individual records matter)</td>
<td style="text-align:center">Pre-aggregated or transformed data to foster better reporting</td>
</tr>
<tr>
<td style="text-align:center">Many users performing varied queries and updates on data across the system</td>
<td style="text-align:center">Fewer users performing deep data analysis with few updates</td>
</tr>
<tr>
<td style="text-align:center">SQL is the primary language for interaction</td>
<td style="text-align:center">Often, but not always, utilizes a particular query language other than SQL</td>
</tr>
</tbody>
</table>

Based on table data, an OLTP database is suitable for us due to the introduction of small or medium amounts of data from
the user. User creation - the user adds the necessary currencies, transactions, . A typical user will not make 1000
transactions per second (limit and verification required).

We can saw on PostgreSQL, MySQL and MariaDB.

### PostgreSQL vs MySQL
<table><thead><tr><th>S.NO.</th><th>MySQL</th><th>PostgreSQL</th></tr></thead><tbody><tr><td>1.</td><td>It is the most <strong>popular</strong> Database.</td><td>It is the most <strong>advanced</strong> Database.</td></tr><tr><td>2.</td><td>It is a <strong>relational-based</strong> DBMS.</td><td>It is an <strong>object-based </strong>relational DBMS</td></tr><tr><td>3.</td><td>It is an ACID-compliant only when used with InnoDB and NDB cluster engines</td><td>It is an ACID-compliant from the ground up.</td></tr><tr><td>4.</td><td>The implementation language is <strong>C/C++</strong>.</td><td>The implementation language is <strong>C</strong>.</td></tr><tr><td>5.</td><td>It supports the CASCADE option.</td><td>CASCADE option is supported.</td></tr><tr><td>6.</td><td>GUI tool provided is <strong>MySQL Workbench</strong></td><td><strong>PgAdmin</strong> is provided</td></tr><tr><td>7.</td><td>It does not support partial, bitmap, and expression indexes.</td><td>It supports all of these</td></tr><tr><td>8.</td><td>It doesn’t provide support for Materialised views and Table inheritance.</td><td>PostgreSQL provides both of them.</td></tr><tr><td>9.</td><td>SQL only supports <strong>Standard data types</strong>.</td><td>It supports <strong>Advanced data types</strong> such as arrays, hstore, and user-defined types.</td></tr><tr><td>10.</td><td>SQL provides <strong>limited MVCC support </strong>( in InnoDB)</td><td><strong>Full MVCC</strong> support.</td></tr><tr><td>11.</td><td>It was developed in 1995 by a Swedish company named MySQL AB.</td><td>It was developed at the University of California, Department of Computer Science.</td></tr><tr><td>12.</td><td>It is reliable, simple, and faster.</td><td>It is slower and more complex.</td></tr><tr><td>13.</td><td>Troubleshooting MySQL is easy.</td><td>It is difficult to troubleshoot PostgreSQL.</td></tr><tr><td>14.</td><td>MySQL is licensed beneath GNU GPU.</td><td>PostgreSQL is licensed beneath MIT style.</td></tr><tr><td>15.</td><td>It is best suitable for simple operations like write and reading.</td><td>It is commonly used for large and complex operations.</td></tr><tr><td>16.</td><td>In MySQL, every connection created is an OS thread.</td><td>In PostgreSQL, every connection created is an OS process.</td></tr></tbody></table>

### PostgreSQL vs MariaDB
<table><tbody><tr><td>&nbsp; &nbsp; &nbsp; &nbsp; <strong>&nbsp;Feature</strong></td><td> <strong>Use-case-Impact</strong></td><td><strong>Use-case-Impact</strong></td></tr><tr><td></td><td>&nbsp; <strong>&nbsp;MariaDB</strong></td><td><strong>&nbsp; &nbsp; PostgreSQL</strong></td></tr><tr><td><strong>Size</strong></td><td>Suits smaller databases</td><td>Suits bigger databases&nbsp;</td></tr><tr><td><strong>Data typing</strong></td><td>Flexible data types&nbsp;</td><td>Strict data integrity</td></tr><tr><td><strong>Replication</strong></td><td>Versatile and powerful</td><td>Only Master-Slave</td></tr><tr><td><strong>Materialized Views</strong>, <strong>Partial Indexes</strong></td><td>Not supported</td><td>Quicker complex queries, Faster aggregations&nbsp;</td></tr><tr><td><strong>Partitioning</strong></td><td>Faster access to partitioned data&nbsp;</td><td>Not supported</td></tr><tr><td><strong>NoSQL and JSon</strong></td><td>Not fully supported</td><td>Suits NoSQL databases&nbsp;</td></tr></tbody></table>

Based on the table data, we can choose **PostgreSQL**, because it is more advanced, free, stable and supports more features with strict data integrity.
