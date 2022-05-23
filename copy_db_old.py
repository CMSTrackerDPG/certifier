from oms.utils import oms_retrieve_run
from certifier.models import RunReconstruction, TrackerCertification, Dataset
from users.models import User
from django.contrib.auth import get_user_model
from django.utils import formats
from shiftleader.utilities.utilities import to_date
import datetime
from dateutil.parser import parse
import maya
import dateutil.parser
import io
import pandas as pd
import psycopg2


def get_referenceruns():
    try:
        connection = psycopg2.connect(host="127.0.0.1", database="mytestdb")
        cursor = connection.cursor()
        postgreSQL_select_Query = (
            "select reference_run, lower(reco) from certhelper_referencerun"
        )
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()

        for row in mobile_records:
            try:
                run = oms_retrieve_run(row[0])
                if not RunReconstruction.objects.filter(
                    run__run_number=row[0], reconstruction=row[1]
                ).exists():
                    RunReconstruction.objects.create(
                        run=run, reconstruction=row[1], is_reference=True
                    )
            except IndexError:
                pass

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def get_runs():
    try:
        connection = psycopg2.connect(host="127.0.0.1", database="mytestdb")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select r.run_number, lower(t.reco) from certhelper_runinfo r, certhelper_type t where r.type_id=t.id"
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()

        for row in mobile_records:
            try:
                run = oms_retrieve_run(row[0])
                if not RunReconstruction.objects.filter(
                    run__run_number=row[0], reconstruction=row[1]
                ).exists():
                    RunReconstruction.objects.create(run=run, reconstruction=row[1])
            except IndexError:
                pass

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def get_users():
    try:
        connection = psycopg2.connect(host="127.0.0.1", database="mytestdb")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select u.*, p.extra_data from auth_user u left join certhelper_userprofile p on u.id=p.user_id"
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()

        for row in mobile_records:
            if not get_user_model().objects.filter(username=row[4]).exists():
                user = get_user_model().objects.create(
                    id=int(row[0]),
                    password=row[1],
                    last_login=row[2],
                    is_superuser=row[3],
                    username=row[4],
                    first_name=row[5],
                    last_name=row[6],
                    email=row[7],
                    is_staff=row[8],
                    is_active=row[9],
                    date_joined=row[10],
                    extra_data=row[11],
                )

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def get_trackercertification():
    try:
        connection = psycopg2.connect(host="127.0.0.1", database="mytestdb")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select r.run_number, lower(t.reco), lower(r.trackermap), lower(r.pixel), lower(r.sistrip), lower(r.tracking), r.comment, r.date, ref.reference_run, lower(ref.reco), u.username, r.deleted_at, r.created_at, r.updated_at, r.pixel_lowstat, r.sistrip_lowstat, r.tracking_lowstat, t.dataset from certhelper_runinfo r, certhelper_referencerun ref, auth_user u, certhelper_type t where r.userid_id=u.id and r.reference_run_id=ref.id and r.type_id=t.id"
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()

        print("Print each row and it's columns values")
        for row in mobile_records:
            try:
                run = RunReconstruction.objects.get(
                    run__run_number=row[0], reconstruction=row[1]
                )
                ref_run = RunReconstruction.objects.get(
                    run__run_number=row[8], reconstruction=row[9]
                )
                user = get_user_model().objects.get(username=row[10])

                if not Dataset.objects.filter(dataset=row[17]).exists():
                    dataset = Dataset.objects.create(dataset=row[17])
                else:
                    dataset = Dataset.objects.get(dataset=row[17])

                if not TrackerCertification.objects.filter(
                    runreconstruction=run
                ).exists():
                    trackercertification = TrackerCertification.objects.create(
                        user=user,
                        runreconstruction=run,
                        dataset=dataset,
                        reference_runreconstruction=ref_run,
                        trackermap=row[2],
                        pixel=row[3],
                        strip=row[4],
                        tracking=row[5],
                        pixel_lowstat=row[14],
                        strip_lowstat=row[15],
                        tracking_lowstat=row[16],
                        date=row[7],
                        comment=row[6],
                    )
            except (RunReconstruction.DoesNotExist, get_user_model().DoesNotExist) as e:
                print(row[0], row[1], row[8], row[9], row[10], e)
                pass
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


get_users()
get_referenceruns()
get_runs()
get_trackercertification()
