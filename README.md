# Just in time 2.5: It's about time: Mad dash

Just in time provided a data visualisation project for DUNE exactly when it was needed. Although it worked, it was a small scaled project with no expantion capabilities, and an expandable version of the project was by now long overdue. "It's about time" aims to provide an implementation of the Just in time functionality with code that's easily expandable and much more robust file structure.


## Quick start

### Dev area setup
```sh
# Create a  DBT work area witl local python environment
dbt-create -c <release> <workarea>
cd <workarea>
source env.sh

# Clone just-in-time here

cd justintime
pip install -r requirements.txt
```


### Running Just-in-Time
```sh
cd justintime
source env.sh

```