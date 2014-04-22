pyodata
=======

An OData framework for Python. It will include a full (as much as possible) implementation of the OData Protocol v4.0

While implementing, we will follow the following guidelines:

**1.** The implementation must be as generic as possible regarding data sources. The implementation **MUST NOT** be biased towards a certain type of data source (e.g. raw data from a relational DB, entity from an ORM, etc.)

**2.** The implementation must support extensibility.

**3.** Even tho some parts of OData may remind of SOA (terms like services, endpoints, etc), the implementation should be RESTfull.

**4.** The implementation should make it possible to perform the basic tasks as easy as possible and still support more complex cases, which will be based on the simple, basic cases.

**5.** Keep it simple, address the common cases, keep the option to extend where needed.
