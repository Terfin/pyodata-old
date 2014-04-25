pyodata
=======

An OData framework for Python. It will include a full (as much as possible) implementation of the OData Protocol v4.0

A link to OData protocol documentation: http://www.odata.org/documentation/odata-version-4-0/

Current Version: 0.0.0.0 (Development hasn't started yet)

If you happen to visit this repo and wish to help, please see the list of features below (table) and see their respective issue items. Thanks!
Also, don't hesitate to leave a note regarding anything you see wrong with either the feature requirements, the architecture or the code.

## IMPLEMENTATION GUIDELINES

**1.** The implementation must be as generic as possible regarding data sources. The implementation **MUST NOT** be biased towards a certain type of data source (e.g. raw data from a relational DB, entity from an ORM, etc.)

**2.** The implementation must support extensibility.

**3.** Even tho some parts of OData may remind of SOA (terms like services, endpoints, etc), the implementation should be RESTfull.

**4.** The implementation should make it possible to perform the basic tasks as easy as possible and still support more complex cases, which will be based on the simple, basic cases.

**5.** Keep it simple, address the common cases, keep the option to extend where needed.

**6. No work is to be done on a feature, unless the feature's requirements have been properly documented, reviewed and approved.**

## DEVELOPMENT GUIDELINES

**1.** Document your code. Others have to be able to get a general idea of what your code does.

**2.** Test your code with unit tests. If you feel comfortable with TDD, you may use it instead of regular development.

**3.** Development Cycles will be in the following order (Assuming feature has been designed):

&nbsp;&nbsp;&nbsp;&nbsp;**a.** Coding -> unit testing -> Fixing. (Or use TDD instead)

&nbsp;&nbsp;&nbsp;&nbsp;**b.** Code review. (Everyone can review everyone's code) and ciritcal bug fixes.

&nbsp;&nbsp;&nbsp;&nbsp;**c.** Component testing and critical bug fixes.

&nbsp;&nbsp;&nbsp;&nbsp;**d.** System and regression testing and fixing critical bugs.

&nbsp;&nbsp;&nbsp;&nbsp;**e.** System of systems testing and regression testing (Of the entire framework) and fix critical bugs.

&nbsp;&nbsp;&nbsp;&nbsp;**f.** Release. (alpha, beta, RC or final)

&nbsp;&nbsp;&nbsp;&nbsp;Of course each testing-fixing phase will be executed over and over again until it passes.

**4.** Each feature will have its own version code and will be treated as a system. The entire framework will have its own version code.

## Supported Features

|Feature | Status|
|--------|--------|
|[EDM - Entity Data Model](https://github.com/Terfin/pyodata/issues/1) | Design |
|[SM - Service Model](https://github.com/Terfin/pyodata/issues/2) | Requirements written, review needed |
|[Versioning](https://github.com/Terfin/pyodata/issues/3) | Requirements written, review needed |
| Extensibility | Not Started |
| Formats | Not Started |
| Headers Handling | Not Started |
| Response Codes | Not Started |
| Context URL | Not Started |
| Data Servoce Reqiests support | Not Started |
| Security | Not Started |
| Conformance | Not Started |

