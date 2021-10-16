# Prowler: AWS CIS Benchmark Tool

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Requirements and Installation](#requirements-and-installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Advanced Usage](#advanced-usage)
- [Security Hub integration](#security-hub-integration)
- [Fix](#fix)
- [Troubleshooting](#troubleshooting)
- [Extras](#extras)
- [Forensics Ready Checks](#forensics-ready-checks)
- [GDPR Checks](#gdpr-checks)
- [HIPAA Checks](#hipaa-checks)
- [Trust Boundaries Checks](#trust-boundaries-checks)
- [Multi Account and Continuous Monitoring](util/org-multi-account/README.md)
- [Add Custom Checks](#add-custom-checks)
- [Third Party Integrations](#third-party-integrations)
- [Full list of checks and groups](/LIST_OF_CHECKS_AND_GROUPS.md)
- [License](#license)

## Description

Prowler is a command line tool for AWS Security Best Practices Assessment, Auditing, Hardening and Forensics Readiness Tool.

It follows guidelines of the CIS Amazon Web Services Foundations Benchmark (49 checks) and has 40 additional checks including related to GDPR and HIPAA.

Read more about [CIS Amazon Web Services Foundations Benchmark v1.2.0 - 05-23-2018](https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf)

## Features

~140 checks controls covering security best practices across all AWS regions and most of AWS services and related to the next groups:

- Identity and Access Management [group1]
- Logging  [group2]
- Monitoring (14 checks) [group3]
- Networking (4 checks) [group4]
- CIS Level 1 [cislevel1]
- CIS Level 2 [cislevel2]
- Extras (39 checks) *see Extras section* [extras]
- Forensics related group of checks [forensics-ready]
- GDPR [gdpr] Read more [here](#gdpr-checks)
- HIPAA [hipaa] Read more [here](#hipaa-checks)
- Trust Boundaries [trustboundaries] Read more [here](#trustboundaries-checks)

With Prowler you can:

- get a colorful or monochrome report
- a CSV, JSON or JSON ASFF format report
- send findings directly to Security Hub
- run specific checks
- check multiple AWS accounts in parallel or sequentially
- and more! Read examples below

## Requirements and Installation

This script has been written in bash using AWS-CLI and it works in Linux and OSX.

- Make sure the latest version of AWS-CLI is installed on your workstation, and other components needed, with Python pip already installed:

    ```sh
    pip install awscli detect-secrets
    ```

    AWS-CLI can be also installed it using "brew", "apt", "yum" or manually from <https://aws.amazon.com/cli/>, but `detect-secrets` has to be installed using `pip`. You will need to install `jq` to get more accuracy in some checks.

- Make sure jq is installed (example below with "apt" but use a valid package manager for your OS):

    ```sh
    sudo apt install jq
    ```

- Previous steps, from your workstation:

    ```sh
    git clone https://github.com/toniblyx/prowler
    cd prowler
    ```

- Make sure you have properly configured your AWS-CLI with a valid Access Key and Region or declare AWS variables properly (or intance profile):

    ```sh
    aws configure
    ```

    or

    ```sh
    export AWS_ACCESS_KEY_ID="ASXXXXXXX"
    export AWS_SECRET_ACCESS_KEY="XXXXXXXXX"
    export AWS_SESSION_TOKEN="XXXXXXXXX"
    ```

- Those credentials must be associated to a user or role with proper permissions to do all checks. To make sure, add the AWS managed policies, SecurityAudit and ViewOnlyAccess, to the user or role being used.  Policy ARNs are:

    ```sh
    arn:aws:iam::aws:policy/SecurityAudit
    arn:aws:iam::aws:policy/job-function/ViewOnlyAccess
    ```

    > Additional permissions needed: to make sure Prowler can scan all services included in the group *Extras*, make sure you attach also the custom policy [prowler-additions-policy.json](https://github.com/toniblyx/prowler/blob/master/iam/prowler-additions-policy.json) to the role you are using. If you want Prowler to send findings to [AWS Security Hub](https://aws.amazon.com/security-hub), make sure you also attach the custom policy [prowler-security-hub.json](https://github.com/toniblyx/prowler/blob/master/iam/prowler-security-hub.json).

## Usage

1. Run the `prowler` command without options (it will use your environment variable credentials if they exist or will default to using the `~/.aws/credentials` file and run checks over all regions when needed. The default region is us-east-1):

    ```sh
    ./prowler
    ```

    Use `-l` to list all available checks and the groups (sections) that reference them

    If you want to avoid installing dependencies run it using Docker:

    ```sh
    docker run -ti --rm --name prowler --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY --env AWS_SESSION_TOKEN toniblyx/prowler:latest
    ```

1. For custom AWS-CLI profile and region, use the following: (it will use your custom profile and run checks over all regions when needed):

    ```sh
    ./prowler -p custom-profile -r us-east-1
    ```

1. For a single check use option `-c`:

    ```sh
    ./prowler -c check310
    ```

    With Docker:

    ```sh
    docker run -ti --rm --name prowler --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY --env AWS_SESSION_TOKEN toniblyx/prowler:latest "-c check310"
    ```

    or multiple checks separated by comma:

    ```sh
    ./prowler -c check310,check722
    ```

    or all checks but some of them:

    ```sh
    ./prowler -E check42,check43
    ```

    or for custom profile and region:

    ```sh
    ./prowler -p custom-profile -r us-east-1 -c check11
    ```

    or for a group of checks use group name:

    ```sh
    ./prowler -g group1 # for iam related checks
    ```

    or exclude some checks in the group:

    ```sh
    ./prowler -g group4 -E check42,check43
    ```

    Valid check numbers are based on the AWS CIS Benchmark guide, so 1.1 is check11 and 3.10 is check310

## Screenshots

- Sample screenshot of report first lines:

    <img width="1125" alt="screenshot 2016-09-13 16 05 42" src="https://cloud.githubusercontent.com/assets/3985464/18489640/50fe6824-79cc-11e6-8a9c-e788b88a8a6b.png">

- Sample screenshot of single check for check 3.3:

    <img width="1006" alt="screenshot 2016-09-14 13 20 46" src="https://cloud.githubusercontent.com/assets/3985464/18522590/a04ca9a6-7a7e-11e6-8730-b545c9204990.png">

- Sample screenshot of the html output `-M html`:
    <img width="1006" alt="Prowler html" src="https://user-images.githubusercontent.com/3985464/82838608-0229ce80-9ecd-11ea-860c-468f66aa2790.png">

### Save your reports

1. If you want to save your report for later analysis thare are different ways, natively (supported text, mono, csv, json, json-asff, junit-xml and html, see note below for more info):

    ```sh
    ./prowler -M csv
    ```

    or with multiple formats at the same time:

    ```sh
    ./prowler -M csv,json,json-asff,html
    ```

    or just a group of checks in multiple formats:

    ```sh
    ./prowler -g gdpr -M csv,json,json-asff
    ```

    or if you want a sorted and dynamic HTML report do:

    ```sh
    ./prowler -M html
    ```

    Now `-M` creates a file inside the prowler `output` directory named `prowler-output-AWSACCOUNTID-YYYYMMDDHHMMSS.format`. You don't have to specify anything else, no pipes, no redirects.

    or just saving the output to a file like below:

    ```sh
    ./prowler -M mono > prowler-report.txt
    ```

    To generate JUnit report files, include the junit-xml format. This can be combined with any other format. Files are written inside a prowler root directory named `junit-reports`:

    ```sh
    ./prowler -M text,junit-xml
    ```

    >Note about output formats to use with `-M`: "text" is the default one with colors, "mono" is like default one but monochrome, "csv" is comma separated values, "json" plain basic json (without comma between lines) and "json-asff" is also json with Amazon Security Finding Format that you can ship to Security Hub using `-S`.

    or save your report in an S3 bucket (this only works for text or mono. For csv, json or json-asff it has to be copied afterwards):

    ```sh
    ./prowler -M mono | aws s3 cp - s3://bucket-name/prowler-report.txt
    ```

    When generating multiple formats and running using Docker, to retrieve the reports, bind a local directory to the container, e.g.:

    ```sh
    docker run -ti --rm --name prowler --volume "$(pwd)":/prowler/output --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY --env AWS_SESSION_TOKEN toniblyx/prowler:latest -M csv,json
    ```

1. To perform an assessment based on CIS Profile Definitions you can use cislevel1 or cislevel2 with `-g` flag, more information about this [here, page 8](https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf):

    ```sh
    ./prowler -g cislevel1
    ```

1. If you want to run Prowler to check multiple AWS accounts in parallel (runs up to 4 simultaneously `-P 4`):

    ```sh
    grep -E '^\[([0-9A-Aa-z_-]+)\]'  ~/.aws/credentials | tr -d '][' | shuf |  \
    xargs -n 1 -L 1 -I @ -r -P 4 ./prowler -p @ -M csv  2> /dev/null  >> all-accounts.csv
    ```

1. For help use:

    ```
    ./prowler -h

    USAGE:
      prowler [ -p <profile> -r <region>  -h ]

      -p <profile>        specify your AWS profile to use (i.e.: default)
      -r <region>         specify an AWS region to direct API requests to
                            (i.e.: us-east-1), all regions are checked anyway if the check requires it
      -c <check_id>       specify one or multiple check ids separated by commas, to see all available checks use -l option
                            (i.e.: check11 for check 1.1 or extra71,extra72 for extra check 71 and extra check 72)
      -g <group_id>       specify a group of checks by id, to see all available group of checks use -L
                            (i.e.: check3 for entire section 3, level1 for CIS Level 1 Profile Definitions or forensics-ready)
      -f <filterregion>   specify an AWS region to run checks against
                            (i.e.: us-west-1)
      -m <maxitems>       specify the maximum number of items to return for long-running requests (default: 100)
      -M <mode>           output mode: text (default), mono, json, json-asff, junit-xml, csv. They can be used combined comma separated.
                            (separator is ,; data is on stdout; progress on stderr).
      -k                  keep the credential report
      -n                  show check numbers to sort easier
                            (i.e.: 1.01 instead of 1.1)
      -l                  list all available checks only (does not perform any check). Add -g <group_id> to only list checks within the specified group
      -L                  list all groups (does not perform any check)
      -e                  exclude group extras
      -E                  execute all tests except a list of specified checks separated by comma (i.e. check21,check31)
      -b                  do not print Prowler banner
      -s                  show scoring report
      -S                  send check output to AWS Security Hub - only valid when the output mode is json-asff (i.e. -M json-asff -S)
      -x                  specify external directory with custom checks (i.e. /my/own/checks, files must start by check)
      -q                  suppress info messages and passing test output
      -A                  account id for the account where to assume a role, requires -R and -T
                            (i.e.: 123456789012)
      -R                  role name to assume in the account, requires -A and -T
                            (i.e.: ProwlerRole)
      -T                  session duration given to that role credentials in seconds, default 1h (3600) recommended 12h, requires -R and -T
                            (i.e.: 43200)
      -I                  External ID to be used when assuming roles (not mandatory), requires -A and -R
      -w                  whitelist file. See whitelist_sample.txt for reference and format
                            (i.e.: whitelist_sample.txt)
      -V                  show version number & exit
      -h                  this help
    ```

## Advanced Usage

### Assume Role:

Prowler uses the AWS CLI underneath so it uses the same authentication methods. However, there are few ways to run Prowler against multiple accounts using IAM Assume Role feature depending on eachg use case. You can just set up your custom profile inside `~/.aws/config` with all needed information about the role to assume then call it with `./prowler -p your-custom-profile`. Additionally you can use `-A 123456789012` and `-R RemoteRoleToAssume` and Prowler will get those temporary credentials using `aws sts assume-role`, set them up as environment variables and run against that given account.

```sh
./prowler -A 123456789012 -R ProwlerRole
```

```sh
./prowler -A 123456789012 -R ProwlerRole -I 123456
```

> *NOTE 1 about Session Duration*: By default it gets credentials valid for 1 hour (3600 seconds). Depending on the mount of checks you run and the size of your infrastructure, Prowler may require more than 1 hour to finish. Use option `-T <seconds>`  to allow up to 12h (43200 seconds). To allow more than 1h you need to modify *"Maximum CLI/API session duration"* for that particular role, read more [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html#id_roles_use_view-role-max-session).

> *NOTE 2 about Session Duration*: Bear in mind that if you are using roles assumed by role chaining there is a hard limit of 1 hour so consider not using role chaining if possible, read more about that, in foot note 1 below the table [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html).

For example, if you want to get only the fails in CSV format from all checks regarding RDS without banner from the AWS Account 123456789012 assuming the role RemoteRoleToAssume and set a fixed session duration of 1h:

```sh
./prowler -A 123456789012 -R RemoteRoleToAssume -T 3600 -b -M cvs -q -g rds
```

```sh
./prowler -A 123456789012 -R RemoteRoleToAssume -T 3600 -I 123456 -b -M cvs -q -g rds
```

### Assume Role and across all accounts in AWS Organizations:

If you want to run Prowler or just a check or a group across all accounts of AWS Organizations you can do this:

First get a list of accounts:
```
ACCOUNTS_IN_ORGS=$(aws organizations list-accounts --query Accounts[*].Id --output text)
```
Then run Prowler to assume a role (same in all members) per each account, in this example it is just running one particular check:
```
for accountId in $ACCOUNTS_IN_ORGS; do ./prowler -A $accountId -R RemoteRoleToAssume -c extra79; done
```

### Custom folder for custom checks

Flag `-x /my/own/checks` will include any check in that particular directory. To see how to write checks see [Add Custom Checks](#add-custom-checks) section.

### Show or log only FAILs

In order to remove noise and get only FAIL findings there is a `-q` flag that makes Prowler to show and log only FAILs. It can be combined with any other option.

```sh
./prowler -q -M csv -b
```

### Set the entropy limit for detect-secrets

Sets the entropy limit for high entropy base64 strings from environment variable `BASE64_LIMIT`. Value must be between 0.0 and 8.0, defaults is 4.5.
Sets the entropy limit for high entropy hex strings from environment variable `HEX_LIMIT`. Value must be between 0.0 and 8.0, defaults is 3.0.

```sh
export BASE64_LIMIT=4.5
export HEX_LIMIT=3.0
```

## Security Hub integration

Since version v2.3, Prowler supports natively sending findings to [AWS Security Hub](https://aws.amazon.com/security-hub). This integration allows Prowler to import its findings to AWS Security Hub. With Security Hub, you now have a single place that aggregates, organizes, and prioritizes your security alerts, or findings, from multiple AWS services, such as Amazon GuardDuty, Amazon Inspector, Amazon Macie, AWS Identity and Access Management (IAM) Access Analyzer, and AWS Firewall Manager, as well as from AWS Partner solutions and now from Prowler. It is as simple as running the command below:

```sh
./prowler -M json-asff -S
```

There are two requirements:

1. Security Hub must be enabled for the active region from where you are calling Prowler (if no region is used with `-r` then `us-east-1` is used). It can be enabled by calling `aws securityhub enable-security-hub`
2. As mentioned in section "Custom IAM Policy", to allow Prowler to import its findings to AWS Security Hub you need to add the policy below to the role or user running Prowler:
    - [iam/prowler-security-hub.json](iam/prowler-security-hub.json)

>Note: to have updated findings in Security Hub you have to run Prowler periodically. Once a day or every certain amount of hours.

## Whitelist or remove FAIL from resources

Sometimes you may find resources that are intentionally configured in a certain way that may be a bad practice but it is all right with it, for example an S3 bucket open to the internet hosting a web site, or a security group with an open port needed in your use case. Now you can use `-w whitelist_sample.txt` and add your resources as `checkID:resourcename` as in this command:

```
./prowler -w whitelist_sample.txt
```

Whitelist option works along with other options and adds a `WARNING` instead of `INFO`, `PASS` or `FAIL` to any output format except for `json-asff`.

## How to fix every FAIL

Check your report and fix the issues following all specific guidelines per check in <https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf>

## Troubleshooting

### STS expired token

If you are using an STS token for AWS-CLI and your session is expired you probably get this error:

```sh
A client error (ExpiredToken) occurred when calling the GenerateCredentialReport operation: The security token included in the request is expired
```

To fix it, please renew your token by authenticating again to the AWS API, see next section below if you use MFA.

### Run Prowler with MFA protected credentials

To run Prowler using a profile that requires MFA you just need to get the session token before hand. Just make sure you use this command:

```sh
aws --profile <YOUR_AWS_PROFILE> sts get-session-token --duration 129600 --serial-number <ARN_OF_MFA> --token-code <MFA_TOKEN_CODE> --output text
```

Once you get your token you can export it as environment variable:

```sh
export AWS_PROFILE=YOUR_AWS_PROFILE
export AWS_SESSION_TOKEN=YOUR_NEW_TOKEN
AWS_SECRET_ACCESS_KEY=YOUR_SECRET
export AWS_ACCESS_KEY_ID=YOUR_KEY
```

or set manually up your `~/.aws/credentials` file properly.

There are some helpfull tools to save time in this process like [aws-mfa-script](https://github.com/asagage/aws-mfa-script) or [aws-cli-mfa](https://github.com/sweharris/aws-cli-mfa).

### AWS Managed IAM Policies

[ViewOnlyAccess](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html#jf_view-only-user)
- Use case: This user can view a list of AWS resources and basic metadata in the account across all services. The user cannot read resource content or metadata that goes beyond the quota and list information for resources.
- Policy description: This policy grants List*, Describe*, Get*, View*, and Lookup* access to resources for most AWS services. To see what actions this policy includes for each service, see [ViewOnlyAccess Permissions](https://console.aws.amazon.com/iam/home#policies/arn:aws:iam::aws:policy/job-function/ViewOnlyAccess)

[SecurityAudit](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html#jf_security-auditor)
- Use case: This user monitors accounts for compliance with security requirements. This user can access logs and events to investigate potential security breaches or potential malicious activity.
- Policy description: This policy grants permissions to view configuration data for many AWS services and to review their logs. To see what actions this policy includes for each service, see [SecurityAudit Permissions](https://console.aws.amazon.com/iam/home#policies/arn:aws:iam::aws:policy/SecurityAudit)

### Custom IAM Policy

[Prowler-Additions-Policy](iam/prowler-additions-policy.json)

Some new and specific checks require Prowler to inherit more permissions than SecurityAudit and ViewOnlyAccess to work properly. In addition to the AWS managed policies, "SecurityAudit" and "ViewOnlyAccess", the user/role you use for checks may need to be granted a custom policy with a few more read-only permissions (to support additional services mostly). Here is an example policy with the additional rights, "Prowler-Additions-Policy" (see below bootstrap script for set it up):

- [iam/prowler-additions-policy.json](iam/prowler-additions-policy.json)

[Prowler-Security-Hub Policy](iam/prowler-security-hub.json)

Allows Prowler to import its findings to [AWS Security Hub](https://aws.amazon.com/security-hub). More information in [Security Hub integration](#security-hub-integration):

- [iam/prowler-security-hub.json](iam/prowler-security-hub.json)

### Bootstrap Script

Quick bash script to set up a "prowler" IAM user with "SecurityAudit" and "ViewOnlyAccess" group with the required permissions (including "Prowler-Additions-Policy"). To run the script below, you need user with administrative permissions; set the `AWS_DEFAULT_PROFILE` to use that account:

```sh
export AWS_DEFAULT_PROFILE=default
export ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' | tr -d '"')
aws iam create-group --group-name Prowler
aws iam create-policy --policy-name Prowler-Additions-Policy --policy-document file://$(pwd)/iam/prowler-additions-policy.json
aws iam attach-group-policy --group-name Prowler --policy-arn arn:aws:iam::aws:policy/SecurityAudit
aws iam attach-group-policy --group-name Prowler --policy-arn arn:aws:iam::aws:policy/job-function/ViewOnlyAccess
aws iam attach-group-policy --group-name Prowler --policy-arn arn:aws:iam::${ACCOUNT_ID}:policy/Prowler-Additions-Policy
aws iam create-user --user-name prowler
aws iam add-user-to-group --user-name prowler --group-name Prowler
aws iam create-access-key --user-name prowler
unset ACCOUNT_ID AWS_DEFAULT_PROFILE
```

The `aws iam create-access-key` command will output the secret access key and the key id; keep these somewhere safe, and add them to `~/.aws/credentials` with an appropriate profile name to use them with prowler. This is the only time they secret key will be shown.  If you lose it, you will need to generate a replacement.

## Extras

We are adding additional checks to improve the information gather from each account, these checks are out of the scope of the CIS benchmark for AWS but we consider them very helpful to get to know each AWS account set up and find issues on it.

Some of these checks look for publicly facing resources may not actually be fully public due to other layered controls like S3 Bucket Policies, Security Groups or Network ACLs.

To list all existing checks please run the command below:

```sh
./prowler -l
```

>There are some checks not included in that list, they are experimental or checks that takes long to run like `extra759` and `extra760` (search for secrets in Lambda function variables and code).

To check all extras in one command:

```sh
./prowler -g extras
```

or to run just one of the checks:

```sh
./prowler -c extraNUMBER
```

or to run multiple extras in one go:

```sh
./prowler -c extraNumber,extraNumber
```


## Forensics Ready Checks

With this group of checks, Prowler looks if each service with logging or audit capabilities has them enabled to ensure all needed evidences are recorded and collected for an eventual digital forensic investigation in case of incident. List of checks part of this group (you can also see all groups with `./prowler -L`). The list of checks can be seen in the group file at:

[groups/group8_forensics](groups/group8_forensics)

The `forensics-ready` group of checks uses existing and extra checks. To get a forensics readiness report, run this command:

```sh
./prowler -g forensics-ready
```

## GDPR Checks

With this group of checks, Prowler shows result of checks related to GDPR, more information [here](https://github.com/toniblyx/prowler/issues/189). The list of checks can be seen in the group file at:

[groups/group9_gdpr](groups/group9_gdpr)

The `gdpr` group of checks uses existing and extra checks. To get a GDPR report, run this command:

```sh
./prowler -g gdpr
```

## HIPAA Checks

With this group of checks, Prowler shows results of controls related to the "Security Rule" of the Health Insurance Portability and Accountability Act aka [HIPAA](https://www.hhs.gov/hipaa/for-professionals/security/index.html) as defined in [45 CFR Subpart C - Security Standards for the Protection of Electronic Protected Health Information](https://www.law.cornell.edu/cfr/text/45/part-164/subpart-C) within [PART 160 - GENERAL ADMINISTRATIVE REQUIREMENTS](https://www.law.cornell.edu/cfr/text/45/part-160) and [Subpart A](https://www.law.cornell.edu/cfr/text/45/part-164/subpart-A) and [Subpart C](https://www.law.cornell.edu/cfr/text/45/part-164/subpart-C) of PART 164 - SECURITY AND PRIVACY

More information on the original PR is [here](https://github.com/toniblyx/prowler/issues/227).

### Note on Business Associate Addendum's (BAA)

Under the HIPAA regulations, cloud service providers (CSPs) such as AWS are considered business associates. The Business Associate Addendum (BAA) is an AWS contract that is required under HIPAA rules to ensure that AWS appropriately safeguards protected health information (PHI). The BAA also serves to clarify and limit, as appropriate, the permissible uses and disclosures of PHI by AWS, based on the relationship between AWS and our customers, and the activities or services being performed by AWS. Customers may use any AWS service in an account designated as a HIPAA account, but they should only process, store, and transmit protected health information (PHI) in the HIPAA-eligible services defined in the Business Associate Addendum (BAA). For the latest list of HIPAA-eligible AWS services, see [HIPAA Eligible Services Reference](https://aws.amazon.com/compliance/hipaa-eligible-services-reference/).

More information on AWS & HIPAA can be found [here](https://aws.amazon.com/compliance/hipaa-compliance/)

The list of checks showed by this group is as follows, they will be mostly relevant for Subsections [164.306 Security standards: General rules](https://www.law.cornell.edu/cfr/text/45/164.306) and [164.312 Technical safeguards](https://www.law.cornell.edu/cfr/text/45/164.312). Prowler is only able to make checks in the spirit of the technical requirements outlined in these Subsections, and cannot cover all procedural controls required. They be found in the group file at:

[groups/group10_hipaa](groups/group10_hipaa)

The `hipaa` group of checks uses existing and extra checks. To get a HIPAA report, run this command:

```sh
./prowler -g hipaa
```

## Trust Boundaries Checks

### Definition and Terms

The term "trust boundary" is originating from the threat modelling process and the most popular contributor Adam Shostack and author of "Threat Modeling: Designing for Security" defines it as following ([reference](https://adam.shostack.org/uncover.html)):

> Trust boundaries are perhaps the most subjective of all: these represent the border between trusted and untrusted elements. Trust is complex. You might trust your mechanic with your car, your dentist with your teeth, and your banker with your money, but you probably don't trust your dentist to change your spark plugs.

AWS is made to be flexible for service links within and between different AWS accounts, we all know that.

This group of checks helps to analyse a particular AWS account (subject) on existing links to other AWS accounts across various AWS services, in order to identify untrusted links.

### Run
To give it a quick shot just call:

```sh
./prowler -g trustboundaries
```

### Scenarios

Currently this check group supports two different scenarios:

1. Single account environment: no action required, the configuration is happening automatically for you.
2. Multi account environment: in case you environment has multiple trusted and known AWS accounts you maybe want to append them manually to [groups/group16_trustboundaries](groups/group16_trustboundaries) as a space separated list into `GROUP_TRUSTBOUNDARIES_TRUSTED_ACCOUNT_IDS` variable, then just run prowler.

### Coverage

Current coverage of Amazon Web Service (AWS) taken from [here](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html):
| Topic                           | Service    | Trust Boundary                                                            |
|---------------------------------|------------|---------------------------------------------------------------------------|
| Networking and Content Delivery | Amazon VPC | VPC endpoints connections ([extra786](checks/check_extra786))             |
|                                 |            | VPC endpoints whitelisted principals ([extra787](checks/check_extra787))  |

All ideas or recommendations to extend this group are very welcome [here](https://github.com/toniblyx/prowler/issues/new/choose).

### Detailed Explanation of the Concept

The diagrams depict two common scenarios, single account and multi account environments.
Every circle represents one AWS account.
The dashed line represents the trust boundary, that separates trust and untrusted AWS accounts.
The arrow simply describes the direction of the trust, however the data can potentially flow in both directions.

Single Account environment assumes that only the AWS account subject to this analysis is trusted. However there is a chance that two VPCs are existing within that one AWS account which are still trusted as a self reference.
![single-account-environment](/docs/images/prowler-single-account-environment.png)

Multi Account environments assumes a minimum of two trusted or known accounts. For this particular example all trusted and known accounts will be tested. Therefore `GROUP_TRUSTBOUNDARIES_TRUSTED_ACCOUNT_IDS` variable in [groups/group16_trustboundaries](groups/group16_trustboundaries) should include all trusted accounts Account #A, Account #B, Account #C, and Account #D in order to finally raise Account #E and Account #F for being untrusted or unknown.
![multi-account-environment](/docs/images/prowler-multi-account-environment.png)

## Add Custom Checks

In order to add any new check feel free to create a new extra check in the extras group or other group. To do so, you will need to follow these steps:

1. Follow structure in file `checks/check_sample`
2. Name your check with a number part of an existing group or a new one
3. Save changes and run it as `./prowler -c extraNN`
4. Send me a pull request! :)

## Add Custom Groups

1. Follow structure in file `groups/groupN_sample`
1. Name your group with a non existing number
1. Save changes and run it as `./prowler -g extraNN`
1. Send me a pull request! :)

- You can also create a group with only the checks that you want to perform in your company, for instance a group named `group9_mycompany` with only the list of checks that you care or your particular compliance applies.

## Third Party Integrations

### AWS Security Hub

There is a blog post about that integration in the AWS Security blog here <https://aws.amazon.com/blogs/security/use-aws-fargate-prowler-send-security-configuration-findings-about-aws-services-security-hub/>

### Telegram

Javier Pecete has done an awesome job integrating Prowler with Telegram, you have more details here <https://github.com/i4specete/ServerTelegramBot>

### Cloud Security Suite

The guys of SecurityFTW have added Prowler in their Cloud Security Suite along with other cool security tools <https://github.com/SecurityFTW/cs-suite>

## License

All CIS based checks in the checks folder are licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License.
The link to the license terms can be found at
<https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode>
Any other piece of code is licensed as Apache License 2.0 as specified in each file. You may obtain a copy of the License at
<http://www.apache.org/licenses/LICENSE-2.0>

NOTE: If you are interested in using Prowler for commercial purposes remember that due to the CC4.0 license “The distributors or partners that are interested and using Prowler would need to enroll as CIS SecureSuite Members to incorporate this product, which includes references to CIS resources, in their offering.". Information about CIS pricing for vendors here: <https://www.cisecurity.org/cis-securesuite/pricing-and-categories/product-vendor/>

**I'm not related anyhow with CIS organization, I just write and maintain Prowler to help companies over the world to make their cloud infrastructure more secure.**

If you want to contact me visit <https://blyx.com/contact>

