import glob
import os

import polib

from django.core.management import BaseCommand, CommandError
from django.core.management.commands.compilemessages import has_bom
from django.core.management.utils import is_ignored_path


class Command(BaseCommand):
    # pylint: disable=missing-class-docstring
    help = 'Check .po ratio of translated messages.'

    requires_system_checks = False

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout=None, stderr=None, no_color=False, force_color=False)
        self.has_errors = False
        self.verbosity = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--locale', '-l', action='append', default=[],
            help='Locale(s) to process (e.g. de_AT). Default is to process all. '
                 'Can be used multiple times.',
        )
        parser.add_argument(
            '--exclude', '-x', action='append', default=[],
            help='Locales to exclude. Default is none. Can be used multiple times.',
        )

        parser.add_argument(
            '--ignore', '-i', action='append', dest='ignore_patterns',
            default=[], metavar='PATTERN',
            help='Ignore directories matching this glob-style pattern. '
                 'Use multiple times to ignore more.',
        )

    @staticmethod
    def get_basedirs(ignore_patterns):
        """Build directories set to explore """
        basedirs = [os.path.join('conf', 'locale'), 'locale']
        if os.environ.get('DJANGO_SETTINGS_MODULE'):
            # pylint: disable=import-outside-toplevel
            from django.conf import settings
            basedirs.extend(settings.LOCALE_PATHS)
        # Walk entire tree, looking for locale directories
        for dirpath, dirnames, _ in os.walk('.', topdown=True):
            for dirname in dirnames:
                if is_ignored_path(os.path.normpath(os.path.join(dirpath, dirname)), ignore_patterns):
                    dirnames.remove(dirname)
                elif dirname == 'locale':
                    basedirs.append(os.path.join(dirpath, dirname))
        # Gather existing directories.
        basedirs = set(map(os.path.abspath, filter(os.path.isdir, basedirs)))
        if not basedirs:
            raise CommandError("This script should be run from the Django Git "
                               "checkout or your project or app tree, or with "
                               "the settings module specified.")
        return basedirs

    # pylint: disable=too-many-locals
    def handle(self, *args, **options):
        locale = options['locale']
        exclude = options['exclude']
        ignore_patterns = set(options['ignore_patterns'])
        self.verbosity = options['verbosity']

        basedirs = self.get_basedirs(ignore_patterns)

        # Build locale list
        all_locales = []
        for basedir in basedirs:
            locale_dirs = filter(os.path.isdir, glob.glob('%s/*' % basedir))
            all_locales.extend(map(os.path.basename, locale_dirs))

        # Account for excluded locales
        locales = locale or all_locales
        locales = set(locales).difference(exclude)

        for basedir in basedirs:
            if locales:
                dirs = [os.path.join(basedir, locale, 'LC_MESSAGES') for locale in locales]
            else:
                dirs = [basedir]
            locations = []
            for ldir in dirs:
                for dirpath, _, filenames in os.walk(ldir):
                    locations.extend((dirpath, f) for f in filenames if f.endswith('.po'))
            if locations:
                self.check_po_content(locations)

        if self.has_errors:
            raise CommandError('compilemessages generated one or more errors.')

    def check_po_content(self, locations):
        """
        Locations is a list of tuples: [(directory, file), ...]
        """
        for dirpath, filename in locations:
            if self.verbosity > 0:
                self.stdout.write('processing file %s in %s\n' % (filename, dirpath))
            po_path = os.path.join(dirpath, filename)
            if has_bom(po_path):
                self.stderr.write(
                    'The %s file has a BOM (Byte Order Mark). Django only '
                    'supports .po files encoded in UTF-8 and without any BOM.' % po_path
                )
                self.has_errors = True
                continue
            # pylint: disable=invalid-name
            po = polib.pofile(po_path)
            if po.untranslated_entries():
                for entry in po.untranslated_entries():
                    self.stdout.write(self.style.WARNING(f'Missing translation for: {entry.msgid}, {entry.msgstr}'))
            if po.percent_translated() == 100:
                self.stdout.write(self.style.SUCCESS(f'translated at {po.percent_translated()}%'))
            else:
                self.stdout.write(self.style.ERROR(f'translated at {po.percent_translated()}%'))
                self.has_errors = True
