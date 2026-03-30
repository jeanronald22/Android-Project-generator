"""
composeforge.templates.kotlin.tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit test and instrumented test templates.
"""


def kt_example_unit_test(pkg: str) -> str:
    """Génère ExampleUnitTest.kt (test unitaire local).

    Args:
        pkg: Package racine du projet.
    """
    return f"""\
package {pkg}

import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * Tests unitaires locaux (JVM).
 * Voir [testing documentation](http://d.android.com/tools/testing).
 */
class ExampleUnitTest {{

    @Test
    fun addition_isCorrect() {{
        assertEquals(4, 2 + 2)
    }}
}}
"""


def kt_example_instrumented_test(pkg: str) -> str:
    """Génère ExampleInstrumentedTest.kt (test Android).

    Args:
        pkg: Package racine du projet.
    """
    return f"""\
package {pkg}

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Tests instrumentés (exécutés sur un appareil Android).
 * Voir [testing documentation](http://d.android.com/tools/testing).
 */
@RunWith(AndroidJUnit4::class)
class ExampleInstrumentedTest {{

    @Test
    fun useAppContext() {{
        val appContext = InstrumentationRegistry.getInstrumentation().targetContext
        assertEquals("{pkg}", appContext.packageName)
    }}
}}
"""
